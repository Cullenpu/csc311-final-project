from csc311_final_project.utils import *
from pdb import set_trace
import numpy as np


def sigmoid(x):
    """ Apply sigmoid function.
    """
    return np.exp(x) / (1 + np.exp(x))


def neg_log_likelihood(data, theta, beta):
    """ Compute the negative log-likelihood.

    You may optionally replace the function arguments to receive a matrix.

    :param sparse: A 542*1774 sparse matrix representing the data
    :param data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param theta: Vector representing the ability of student i
    :param beta: Vector representing the difficulty of problem j
    :return: float
    """
    log_like = 0.
    for i in range(len(theta)):
        for j in range(len(beta)):
            diff = theta[i] - beta[j]
            inner_sum = diff - np.log((1 + np.exp(diff)))
            log_like += inner_sum
    return -log_like


def get_theta_deriv(theta, beta):
    N, D = len(theta), len(beta)
    theta_deriv = np.zeros(N)
    for i in range(N):
        theta_vector = np.full(D, theta[i])
        exp = np.exp(theta_vector - beta)
        inner = np.ones(D) - (exp/(np.ones(D) + exp))
        theta_deriv[i] = np.sum(inner)
    return theta_deriv


def get_beta_deriv(theta, beta):
    N, D = len(theta), len(beta)
    beta_deriv = np.zeros(D)
    for i in range(D):
        beta_vector = np.full(N, beta[i])
        exp = np.exp(theta - beta_vector)
        inner = (exp / (np.ones(N) + exp)) - np.ones(N)
        beta_deriv[i] = np.sum(inner)
    return beta_deriv


def update_theta_beta(data, lr, theta, beta):
    """ Update theta and beta using gradient descent.

    You are using alternating gradient descent. Your update should look:
    for i in iterations ...
        theta <- new_theta
        beta <- new_beta

    You may optionally replace the function arguments to receive a matrix.

    :param data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param lr: float
    :param theta: Vector
    :param beta: Vector
    :return: tuple of vectors
    """
    for i in range(10):
        theta = theta - lr * get_theta_deriv(theta, beta)
        beta = beta - lr * get_beta_deriv(theta, beta)
    return theta, beta


def irt(sparse_matrix, data, val_data, lr, iterations):
    """ Train IRT model.

    You may optionally replace the function arguments to receive a matrix.

    :param data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param val_data: A dictionary {user_id: list, question_id: list,
    is_correct: list}
    :param lr: float
    :param iterations: int
    :return: (theta, beta, val_acc_lst)
    """
    theta = np.zeros(sparse_matrix.shape[0])
    beta = np.zeros(sparse_matrix.shape[1])

    val_acc_lst = []

    for i in range(iterations):
        neg_lld = neg_log_likelihood(data, theta=theta, beta=beta)
        score = evaluate(data=val_data, theta=theta, beta=beta)
        val_acc_lst.append(score)
        print("NLLK: {} \t Score: {}".format(neg_lld, score))
        theta, beta = update_theta_beta(data, lr, theta, beta)

    # TODO: You may change the return values to achieve what you want.
    return theta, beta, val_acc_lst


def evaluate(data, theta, beta):
    """ Evaluate the model given data and return the accuracy.
    :param data: A dictionary {user_id: list, question_id: list,
    is_correct: list}

    :param theta: Vector
    :param beta: Vector
    :return: float
    """
    pred = []
    for i, q in enumerate(data["question_id"]):
        u = data["user_id"][i]
        x = (theta[u] - beta[q]).sum()
        p_a = sigmoid(x)
        pred.append(p_a >= 0.5)
    return np.sum((data["is_correct"] == np.array(pred))) \
           / len(data["is_correct"])


def main():
    train_data = load_train_csv("../data")
    # You may optionally use the sparse matrix.
    sparse_matrix = load_train_sparse("../data")
    val_data = load_valid_csv("../data")
    test_data = load_public_test_csv("../data")

    #####################################################################
    # TODO:                                                             #
    # Tune learning rate and number of iterations. With the implemented #
    # code, report the validation and test accuracy.                    #
    #####################################################################
    irt(sparse_matrix, train_data, val_data, 0.1, 10)
    #####################################################################
    #                       END OF YOUR CODE                            #
    #####################################################################

    #####################################################################
    # TODO:                                                             #
    # Implement part (c)                                                #
    #####################################################################
    pass
    #####################################################################
    #                       END OF YOUR CODE                            #
    #####################################################################


if __name__ == "__main__":
    main()
