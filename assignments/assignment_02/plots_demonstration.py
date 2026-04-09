import matplotlib.pyplot as plt


def lr_key(lr: float) -> str:
    return int(lr * 10)


LEARNING_RATES = [0.01, 0.03, 0.1, 0.4, 1.0]
BATCH_SIZES = [25, 50, 100, 200]
BATCH_SIZE = 25  # Optimal batch size, for testing LR impact
LR = 0.4  # Optimal LR, for testing batch size impact

VAL_LOSS = "val_loss"


def loss_multiple_plots(results: dict):
    epochs = [i for i in range(len(results[lr_key(LR)][BATCH_SIZE]))]

    # Get the learning rates curves
    lr_res = {}
    for lr in LEARNING_RATES:
        lrk = lr_key(lr)
        lr_res[lrk] = [res[VAL_LOSS] for res in results[lrk][BATCH_SIZE]]

    # Get the batch size curves
    lrk = lr_key(LR)
    bs_res = {}
    for bs in BATCH_SIZES:
        bs_res[bs] = [res[VAL_LOSS] for res in results[lrk][bs]]

    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # , sharey=True)

    # ---- Left plot ----
    for lr in LEARNING_RATES:
        lrk = lr_key(lr)
        axes[0].plot(epochs, lr_res[lrk], marker="o", label=f"{lr:.2f}")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("validation loss")
    axes[0].set_title("Val Loss vs Epoch (LR)")
    axes[0].grid(True)
    axes[0].legend()

    # ---- Right plot ----
    lrk = lr_key(LR)
    for bs in BATCH_SIZES:
        axes[1].plot(epochs, bs_res[bs], marker="o", label=f"{bs}")
    axes[1].set_xlabel("epoch")
    axes[1].set_ylabel("validation loss")
    axes[1].set_title("Val Loss vs Epoch (BS)")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def sparsity_plot(non_zeros: list, accuracies: list):
    lambdas = [x[0] for x in non_zeros]
    lambdas[0] = 1e-5
    train_acc = [x[1] for x in accuracies]
    val_acc = [x[2] for x in accuracies]
    nons = [x[1] for x in non_zeros]

    # Create figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # ---- Left plot ----
    axes[0].plot(lambdas, train_acc, marker="o", label="train")
    axes[0].plot(lambdas, val_acc, marker="o", label="validation")
    axes[0].set_xlabel("lambdas")
    axes[0].set_ylabel("accuracy")
    axes[0].set_title("Accuracy vs Reg Lambda")
    axes[0].grid(True)
    axes[0].legend()

    # ---- Right plot ----
    axes[1].plot(lambdas, nons, marker="o", label="none zero")
    axes[1].set_xlabel("lambda")
    axes[1].set_ylabel("None Zero Weights")
    axes[1].set_title("Sparsity vs. Reg Lambda")
    axes[1].grid(True)
    axes[1].legend()

    for ax in axes:
        ax.set_xscale("log")

    plt.tight_layout()
    plt.show()
