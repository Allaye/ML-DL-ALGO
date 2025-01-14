import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision


class LeNet(nn.Module):
    """
    implementation of the LeNet5 architecture as proposed by Yann Lecun and others,
    see https://en.wikipedia.org/wiki/LeNet-5
    this implementation might just be close as possible to the original implementation

    """

    def __init__(self) -> None:
        """
        instantiate the LeNet5 architecture
        :param self: class instance
        :rtype: None
        """
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, stride=1, padding=0)
        self.conv2 = nn.Conv2d(6, 16, 5, 1)
        self.conv3 = nn.Conv2d(16, 120, 5, 1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(in_features=120, out_features=84)
        self.fc2 = nn.Linear(84, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        pass the input through the network, in their respective layers and order and return the output
        :param x: input
        :rtype: torch.Tensor
        """
        x = self.pool(F.relu(input=self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        x = x.reshape(x.shape[0], -1)  # x.reshape[0], -1 flatten the output of the convolutional layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def loss_optimizer(self, lr=0.001) -> tuple:
        """
        define the loss and optimizer
        :param lr: learning rate
        :rtype: tuple of torch.nn.CrossEntropyLoss and torch.optim.SGD
        """
        # define the loss function
        loss_fn = nn.CrossEntropyLoss()
        # define the optimizer
        optimizer = torch.optim.Adam(self.parameters(), lr)
        return loss_fn, optimizer

# if __name__ == "__main__":
#     # load hyper parameters
#     learning_rate, epochs, batch_size = hyperparameter()

#     # load dataset
#     train_loader, test_loader, classes = prepare_dataset(batch_size)

#     # configure device
#     device = configure_device()

#     # instantiate the model
#     model = LeNet().to(device)

#     # define loss and optimizer 
#     loss_fn, optimizer = model.loss_optimizer(lr=learning_rate)

#     # train the model
#     train(model, train_loader, test_loader, epochs, loss_fn, device, batch_size, optimizer)
