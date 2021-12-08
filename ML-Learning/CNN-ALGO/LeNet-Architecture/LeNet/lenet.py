import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms


def configure_device():
    '''
    check if GPU is available and use it
    '''
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device:", device)
    return device


def hyperparameter():
    '''
    define hyper parameters
    '''
    lr = 0.001
    epochs = 10
    batch_size = 100
    return lr, epochs, batch_size


def prepare_dataset(batch_size):
    '''
    get the CIFAR10 dataset, transform it to tensor and normalize it
    '''
    # MNIST dataset
    train_dataset = torchvision.datasets.CIFAR10(root='./',train=True,
                                               transform=transforms.ToTensor(),
                                               download=False)
    test_dataset = torchvision.datasets.CIFAR10(root='./', train=False, transform=transforms.ToTensor())
    
    # Data loader
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    return train_loader, test_loader, classes

a, b, c = prepare_dataset(100)
print(len(a))
# for i, (image, lable) in enumerate(a):
#     print(image.shape)
#     print(lable)
#     break

class LeNet(nn.Module):
    '''
    implementation of the LeNet5 architecture as proposed by Yann Lecun and others,
    see https://en.wikipedia.org/wiki/LeNet-5
    this implementation might just be close as possible to the original implementation
    
    '''
    def __init__(self):
        '''
        instantiate the LeNet5 architecture
        '''
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5, 1)
        self.conv2 = nn.Conv2d(6, 16, 5, 1)
        self.conv3 = nn.Conv2d(16, 120, 5, 1)
        self.pool = nn.AvgPool2d(2, 2)
        self.fc1 = nn.Linear(120, 84)
        self.fc2 = nn.Linear(84, 10)

    def forward(self, x):
        '''
        pass the input through the network, in there respective layers and order and return the output
        '''
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 120) # x.reshape[0], -1 flatten the output of the convolutional layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

    def loss_optimizer(self, lr=0.001):
        '''
        define the loss and optimizer
        '''
        # define the loss function
        loss_fn = nn.CrossEntropyLoss()
        # define the optimizer
        optimizer = torch.optim.Adam(self.parameters(), lr)
        return loss_fn, optimizer


def train(model, train_loader, test_loader, epochs, loss_fn, device, batch_size, optimizer):
    '''
    perform model training loop and hyperparameter tuning
    '''
    n_total_steps = len(train_loader)
    for epoch in range(epochs):
        for i, (images, labels) in enumerate(train_loader):
            # move tensors to the configured device
            images = images.to(device)
            labels = labels.to(device)
            # perform a forward pass
            outputs = model(images)

            # calculate the loss
            loss = loss_fn(outputs, labels)

            # clear the gradients and perform a backward and optimize step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # print training statistics and other information
            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{epochs}], Step [{i + 1}/{n_total_steps}], Loss: {loss.item():.4f}')


def model_eval(model, test_loader, device, batch_size):
    '''
    perform model evaluation and testing using the test dataset
    '''
    # disengage the model from tracking the gradients
    with torch.no_grad():
        # initialize variables
        test_loss = 0
        correct = 0
        total = 0
        # loop over the test set
        for images, labels in test_loader:
            # move tensors to the configured device
            images = images.to(device)
            labels = labels.to(device)
            # perform a forward pass
            outputs = model(images)
            # calculate the loss
            test_loss += F.cross_entropy(outputs, labels, reduction='sum').item()
            # calculate the number of correct predictions
            pred = outputs.max(1, keepdim=True)[1]
            correct += pred.eq(labels.view_as(pred)).sum().item()
            # calculate the total number of test images
            total += labels.size(0)
        # calculate the average test loss and accuracy
        test_loss /= total
        accuracy = 100. * correct / total
        # print the average test loss and accuracy
        print(f'Test Loss: {test_loss:.4f}, Accuracy: {accuracy:.2f}%')
        return accuracy
    '''
    perform model evaluation and return the accuracy
    '''
    # set the model to evaluation mode
    model.eval()
    # track the number of correct predictions
    correct = 0
    # track the number of images
    total = 0
    # iterate over the test dataset
    with torch.no_grad():
        for data in test_loader:
            # get the images and labels
            images, labels = data[0].to(device), data[1].to(device)
            # forward pass
            outputs = model(images)
            # get the predictions
            _, predicted = torch.max(outputs.data, 1)
            # calculate the number of correct predictions
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    # calculate the accuracy
    accuracy = 100 * correct / total
    # print the accuracy
    print(f'Accuracy of the network on the 10000 test images: {correct}/{total} ({accuracy:.4f}%)')