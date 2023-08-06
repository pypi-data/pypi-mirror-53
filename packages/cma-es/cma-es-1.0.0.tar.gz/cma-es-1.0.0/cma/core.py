import logging

import numpy as np
import tensorflow as tf


logger = logging.getLogger(__name__)


class CMA(object):
    """
    Covariance Matrix Adaptation Evolution Strategy (CMA-ES) implementation in TensorFlow v2.

    This implementation is essentially following "The CMA Evolution Strategy: A Tutorial" [1]

    [1] https://arxiv.org/abs/1604.00772
    """
    def __init__(
        self,
        initial_solution,
        initial_step_size,
        fitness_function,
        population_size=None,
        enforce_bounds=None,
        termination_no_effect=1e-8,
        store_trace=False,
    ):
        if not isinstance(initial_solution, (np.ndarray, list)):
            raise ValueError('Initial solution must be a list or numpy array')
        elif np.ndim(initial_solution) != 1:
            ndim = np.ndim(initial_solution)
            raise ValueError(f'Initial solution must be a 1D array but got an array of dim {ndim}')
        elif not np.isscalar(initial_step_size) or initial_step_size <= 0:
            raise ValueError(f'Initial step size must be a number greater than zero')
        elif not callable(fitness_function):
            raise ValueError(f'Fitness function must be callable')
        elif population_size is not None and population_size <= 4:
            raise ValueError(f'Population size must be at least 4')
        elif enforce_bounds is not None and not isinstance(enforce_bounds, (np.ndarray, list)):
            raise ValueError('Bounds must be a list or numpy array')
        elif enforce_bounds is not None and np.ndim(enforce_bounds) != 2:
            ndim = np.ndim(enforce_bounds)
            raise ValueError(f'Bounds must be a 2D array but got an array of dim {ndim}')

        self.generation = 0
        self.initial_solution = initial_solution
        self.dimension = len(initial_solution)
        self.initial_step_size = initial_step_size
        self.fitness_fn = fitness_function
        self.population_size = population_size
        self.enforce_bounds = enforce_bounds
        self.termination_no_effect = termination_no_effect
        self.store_trace = store_trace

        if self.store_trace:
            self.trace = []

        self._initialized = False
        self._enforce_bounds = self.enforce_bounds is not None

    def init(self):
        if self._initialized:
            raise ValueError('Already initialized - call reset method to start over')

        # -------------------------
        # Non-trainable parameters
        # -------------------------
        # Solution dimension
        self.N = tf.constant(self.dimension, dtype=tf.float64)
        # Population size
        if self.population_size is not None:
            self.λ = tf.constant(self.population_size, dtype=tf.float64)
        else:
            self.λ = tf.floor(tf.math.log(self.N) * 3 + 8)
        # Shape of the population of solutions
        self.shape = tf.cast((self.λ, self.N), tf.int32)
        # Number of surviving individuals from one generation to the next
        self.μ = tf.floor(self.λ / 2)
        # Recombination weights
        self.weights = tf.concat([
            tf.math.log(self.μ + 0.5) - tf.math.log(tf.range(1, self.μ + 1)),
            tf.zeros(shape=(self.λ - self.μ,), dtype=tf.float64),
        ], axis=0)
        # Normalize weights such as they sum to one and reshape into a column matrix
        self.weights = (self.weights / tf.reduce_sum(self.weights))[:, tf.newaxis]
        # Variance-effective size of mu
        self.μeff = tf.reduce_sum(self.weights) ** 2 / tf.reduce_sum(self.weights ** 2)
        # Time constant for cumulation for C
        self.cc = (4 + self.μeff / self.N) / (self.N + 4 + 2 * self.μeff / self.N)
        # Time constant for cumulation for sigma control
        self.cσ = (self.μeff + 2) / (self.N + self.μeff + 5)
        # Learning rate for rank-one update of C
        self.c1 = 2 / ((self.N + 1.3)**2 + self.μeff)
        # Learning rate for rank-μ update of C
        self.cμ = 2 * (self.μeff - 2 + 1 / self.μeff) / ((self.N + 2)**2 + 2 * self.μeff / 2)
        # Damping for sigma
        self.damps = 1 + 2 * tf.maximum(0, tf.sqrt((self.μeff - 1) / (self.N + 1)) - 1) + self.cσ
        # Expectation of ||N(0,I)||
        self.chiN = tf.sqrt(self.N) * (1 - 1 / (4 * self.N) + 1 / (21 * self.N**2))

        # Define bounds in a format that can be fed to tf.clip_by_value
        if self._enforce_bounds:
            bounds = tf.convert_to_tensor(self.enforce_bounds, dtype=tf.float64)
            self.clip_value_min = bounds[:, 0]
            self.clip_value_max = bounds[:, 1]

        # ---------------------
        # Trainable parameters
        # ---------------------
        # Mean
        self.m = tf.Variable(tf.constant(self.initial_solution, dtype=tf.float64))
        # Step-size
        self.σ = tf.Variable(tf.constant(self.initial_step_size, dtype=tf.float64))
        # Covariance matrix
        self.C = tf.Variable(tf.eye(num_rows=self.N, dtype=tf.float64))
        # Evolution path for σ
        self.p_σ = tf.Variable(tf.zeros((self.N,), dtype=tf.float64))
        # Evolution path for C
        self.p_C = tf.Variable(tf.zeros((self.N,), dtype=tf.float64))
        # Coordinate system (normalized eigenvectors)
        self.B = tf.Variable(tf.eye(num_rows=self.N, dtype=tf.float64))
        # Scaling (square root of eigenvalues)
        self.D = tf.Variable(tf.eye(num_rows=self.N, dtype=tf.float64))

        self.generation = 0
        self._initialized = True
        return self

    def search(self, max_generations=500):
        if not self._initialized:
            self.init()

        for _ in range(max_generations):
            self.generation += 1

            # -----------------------------------------------------
            # (1) Sample a new population of solutions ∼ N(m, σ²C)
            # -----------------------------------------------------
            z = tf.random.normal(self.shape, dtype=tf.float64)   # ∼ N(0, I)
            y = tf.matmul(z, tf.matmul(self.B, self.D))          # ∼ N(0, C)
            x = self.m + self.σ * y                              # ∼ N(m, σ²C)

            penalty = 0.
            if self._enforce_bounds:
                x_corr = tf.clip_by_value(x, self.clip_value_min, self.clip_value_max)
                penalty = tf.norm(x - x_corr)**2
                x = x_corr

            # -------------------------------------------------
            # (2) Selection and Recombination: Moving the Mean
            # -------------------------------------------------
            # Evaluate and sort solutions
            f_x = self.fitness_fn(x) + penalty
            x_sorted = tf.gather(x, tf.argsort(f_x))

            if self.store_trace:
                self.trace.append({
                    'm': self.m.read_value().numpy(),
                    'σ': self.σ.read_value().numpy(),
                    'C': self.C.read_value().numpy(),
                    'p_σ': self.p_σ.read_value().numpy(),
                    'p_C': self.p_C.read_value().numpy(),
                    'B': self.B.read_value().numpy(),
                    'D': self.D.read_value().numpy(),
                    'population': x_sorted.numpy(),
                })

            # The new mean is a weighted average of the top-μ solutions
            x_diff = (x_sorted - self.m)
            x_mean = tf.reduce_sum(tf.multiply(x_diff, self.weights), axis=0)
            m = self.m + x_mean

            # -----------------------------------
            # (3) Adapting the Covariance Matrix
            # -----------------------------------
            # Udpdate evolution path for Rank-one-Update
            y_mean = x_mean / self.σ
            p_C = (
                (1 - self.cc) * self.p_C +
                tf.sqrt(self.cc * (2 - self.cc) * self.μeff) * y_mean
            )
            p_C_matrix = p_C[:, tf.newaxis]

            # Compute Rank-μ-Update
            C_m = tf.map_fn(
                fn=lambda e: e * tf.transpose(e),
                elems=(x_diff / self.σ)[:, tf.newaxis],
            )
            y_s = tf.reduce_sum(
                tf.multiply(C_m, self.weights[:, tf.newaxis]),
                axis=0,
            )

            # Combine Rank-one-Update and Rank-μ-Update
            C = (
                (1 - self.c1 - self.cμ) * self.C +
                self.c1 * p_C_matrix * tf.transpose(p_C_matrix) +
                self.cμ * y_s
            )

            # Enforce symmetry of the covariance matrix
            C_upper = tf.linalg.band_part(C, 0, -1)
            C_upper_no_diag = C_upper - tf.linalg.tensor_diag(tf.linalg.diag_part(C_upper))
            C = C_upper + tf.transpose(C_upper_no_diag)

            # ----------------------
            # (4) Step-size control
            # ----------------------
            # Update evolution path for sigma
            D_inv = tf.linalg.tensor_diag(tf.math.reciprocal(tf.linalg.diag_part(self.D)))
            C_inv_squared = tf.matmul(tf.matmul(self.B, D_inv), tf.transpose(self.B))
            C_inv_squared_y = tf.squeeze(tf.matmul(C_inv_squared, y_mean[:, tf.newaxis]))
            p_σ = (
                (1 - self.cσ) * self.p_σ +
                tf.sqrt(self.cσ * (2 - self.cσ) * self.μeff) * C_inv_squared_y
            )

            # Update sigma
            σ = self.σ * tf.exp((self.cσ / self.damps) * ((tf.norm(p_σ) / self.chiN) - 1))

            # ----------------------------------------
            # (5) Update B and D: eigen decomposition
            # ----------------------------------------
            try:
                eigenvalues, eigenvectors = tf.linalg.eigh(C)
            except tf.errors.InvalidArgumentError as e:
                logger.error(e)
                logger.error('Eigen decomposition was not successful - aborting')
                break

            diag_D = tf.sqrt(eigenvalues)
            D = tf.linalg.tensor_diag(diag_D)
            B = eigenvectors

            # -------------------------------
            # (6) Assign new variable values
            # -------------------------------
            # Cache computations necessary to determine termination criteria
            self._prev_sigma = tf.identity(self.σ)
            self._prev_D = tf.identity(self.D)
            self._diag_D = diag_D

            # Assign values
            self.p_C.assign(p_C)
            self.p_σ.assign(p_σ)
            self.C.assign(C)
            self.σ.assign(σ)
            self.B.assign(B)
            self.D.assign(D)
            self.m.assign(m)

            # ---------------------------------
            # (7) Terminate early if necessary
            # ---------------------------------
            if self.termination_criterion_met():
                break

        return self

    def best_solution(self):
        return self.m.read_value().numpy()

    def best_fitness(self):
        return self.fitness_fn(np.array([self.best_solution()]))[0]

    def termination_criterion_met(self, return_details=False):
        # NoEffectAxis: stop if adding a 0.1-standard deviation vector in any principal axis
        # direction of C does not change m
        i = self.generation % self.dimension
        m_nea = self.m + 0.1 * self.σ * tf.squeeze(self._diag_D[i] * self.B[i,:])
        m_nea_diff = tf.abs(self.m - m_nea)
        no_effect_axis = tf.reduce_all(tf.less(m_nea_diff, self.termination_no_effect))

        # NoEffectCoord: stop if adding 0.2 stdev in any single coordinate does not change m
        m_nec = self.m + 0.2 * self.σ * tf.linalg.diag_part(self.C)
        m_nec_diff = tf.abs(self.m - m_nec)
        no_effect_coord = tf.reduce_any(tf.less(m_nec_diff, self.termination_no_effect))

        # ConditionCov: stop if the condition number of the covariance matrix becomes too large
        max_D = tf.reduce_max(self._diag_D)
        min_D = tf.reduce_min(self._diag_D)
        condition_number = max_D**2 / min_D**2
        condition_cov = tf.greater(condition_number, 1e14)

        # TolXUp: stop if σ × max(D) increased by more than 10^4.
        # This usually indicates a far too small initial σ, or divergent behavior.
        prev_max_D = tf.reduce_max(tf.linalg.diag_part(self._prev_D))
        tol_x_up_diff = tf.abs(self.σ * max_D - self._prev_sigma * prev_max_D)
        tol_x_up = tf.greater(tol_x_up_diff, 1e4)

        do_terminate = no_effect_axis or no_effect_coord or condition_cov or tol_x_up

        if not return_details:
            return do_terminate
        else:
            return (
                do_terminate,
                dict(
                    no_effect_axis=bool(no_effect_axis.numpy()),
                    no_effect_coord=bool(no_effect_coord.numpy()),
                    condition_cov=bool(condition_cov.numpy()),
                    tol_x_up=bool(tol_x_up.numpy()),
                )
            )

    def reset(self):
        self._initialized = False
        return self.init()
