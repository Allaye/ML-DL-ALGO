import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    """
    a factory class to create basic convolution network
    """
    def __init__(self, in_channels, out_channels, **kwargs):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, **kwargs)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class InceptionBlock(nn.Module):
    """
    a conv class that uses the convblock to create the inceptionNet block
    """
    def __init__(self, in_channels, out_1x1, out_3x3reduce, out_3x3, out_5x5reduce, out_5x5, out_1x1pool):
        super(InceptionBlock, self).__init__()
        self.incepBlock1 = ConvBlock(in_channels, out_1x1, kernel_size=1, padding='same')
        self.incepBlock3 = nn.Sequential(
            ConvBlock(in_channels, out_3x3reduce, kernel_size=1, padding='same'),
            ConvBlock(out_3x3reduce, out_3x3, kernel_size=3, padding='same'))
        self.incepBlock5 = nn.Sequential(
            ConvBlock(in_channels, out_5x5reduce, kernel_size=1, padding='same'),
            ConvBlock(out_5x5reduce, out_5x5, kernel_size=5, padding=2))
        self.incepBlockpool1 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            ConvBlock(in_channels, out_1x1pool, kernel_size=1, padding='same'))

    def forward(self, x):
        return torch.cat([
            self.incepBlock1(x),
            self.incepBlock3(x),
            self.incepBlock5(x),
            self.incepBlockpool1(x)
        ], 1)


