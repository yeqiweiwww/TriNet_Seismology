
import torch
import torch.nn as nn
import torch.nn.functional as F

from copy import deepcopy

'''
'''


## muticonv_para
muticonv_para = [
    [3, 1, 1],
    [3, 1, 1],
]

## encoder & decoder
begin_end_conv_para = [[2,2], 1, [0,0]]
encoder_decoder_channel_para = [128, 256, 512, 1024]
encoder_decoder_conv_para = [encoder_decoder_channel_para[0], int(encoder_decoder_channel_para[0]/2), int(encoder_decoder_channel_para[0]/4), int(encoder_decoder_channel_para[0]/8)]
unet_decoder_conv_para = [512, 256, 128, 2**len(encoder_decoder_conv_para)*2]

encoder_decoder_linear_para = [512, 256, 128, 64]


def muticonv_block(in_channels, out_channels, kernel_size, stride, padding):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(),
    )

class MutiConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.muticonv = nn.ModuleList()
        for index_para in range(len(muticonv_para)):
            if index_para == 0:
                self.muticonv.append(muticonv_block(in_channels, out_channels, muticonv_para[index_para][0], muticonv_para[index_para][1], muticonv_para[index_para][2]))
            else:
                self.muticonv.append(muticonv_block(out_channels, out_channels, muticonv_para[index_para][0], muticonv_para[index_para][1], muticonv_para[index_para][2]))

        self.initialize_weights()

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)

    def forward(self, x):
        for index_block in range(len(self.muticonv)):
            x = self.muticonv[index_block](x)
        return x

class Encoder_Decoder_Linear(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()


        # self.liner_blocks = nn.Sequential(
        #     nn.Dropout(0.3),
        #     nn.Linear(encoder_decoder_channel_para[0] * pic1 * pic2, decoder_liner_para[0]),
        #     nn.ReLU(),
        #     nn.Dropout(0.3),
        #     nn.Linear(decoder_liner_para[0], decoder_liner_para[1]),
        #     nn.ReLU(),
        #     nn.Dropout(0.3),
        #     nn.Linear(decoder_liner_para[1], decoder_liner_para[2]),
        #     nn.ReLU(),
        #     nn.Linear(decoder_liner_para[2], decoder_liner_para[3]),
        #     nn.Linear(decoder_liner_para[3], out_channels),
        # )

        self.linear1 = nn.Linear(in_channels, encoder_decoder_linear_para[0])
        self.linear2 = nn.Linear(encoder_decoder_linear_para[0], encoder_decoder_linear_para[1])
        self.linear3 = nn.Linear(encoder_decoder_linear_para[1], encoder_decoder_linear_para[2])
        self.linear4 = nn.Linear(encoder_decoder_linear_para[2], encoder_decoder_linear_para[3])
        self.linear5 = nn.Linear(encoder_decoder_linear_para[3], out_channels)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

        self.initialize_weights()

    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)

    def forward(self, output):
        self.training = True
        output = F.dropout(output, 0.3, self.training)
        output = self.linear1(output)
        output = self.relu(output)
        output = F.dropout(output, 0.3, self.training)
        output = self.linear2(output)
        output = self.relu(output)
        output = F.dropout(output, 0.3, self.training)
        output = self.linear3(output)
        output = self.relu(output)
        output = self.linear4(output)
        output = self.linear5(output)
        output = self.tanh(output)

        return output

# class Encoder_Decoder_Conv(nn.Module):
#     def __init__(self, in_channels, out_channels):
#         super().__init__()

#         self.conv1 = nn.Conv1d(in_channels, encoder_decoder_conv_para[0], 3, 2, 1)
#         self.batch1 = nn.BatchNorm1d(encoder_decoder_conv_para[0])
#         self.conv2 = nn.Conv1d(encoder_decoder_conv_para[0], encoder_decoder_conv_para[1], 3, 2, 1)
#         self.batch2 = nn.BatchNorm1d(encoder_decoder_conv_para[1])
#         self.conv3 = nn.Conv1d(encoder_decoder_conv_para[1], encoder_decoder_conv_para[2], 3, 2, 1)
#         self.batch3 = nn.BatchNorm1d(encoder_decoder_conv_para[2])
#         self.conv4 = nn.Conv1d(encoder_decoder_conv_para[2], encoder_decoder_conv_para[3], 3, 2, 1)
#         self.batch4 = nn.BatchNorm1d(encoder_decoder_conv_para[3])
#         self.conv5 = nn.Conv1d(encoder_decoder_conv_para[3], out_channels, 3, 2, 1)
#         self.relu = nn.ReLU()
#         self.tanh = nn.Tanh()

#         self.initialize_weights()

#     def initialize_weights(self):
#         for m in self.modules():
#             if isinstance(m, nn.Conv2d) or isinstance(m, nn.Conv1d):
#                 nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
#                 if m.bias is not None:
#                     nn.init.constant_(m.bias, 0)
#             elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
#                 nn.init.constant_(m.weight, 1)
#                 nn.init.constant_(m.bias, 0)
#             elif isinstance(m, nn.Linear):
#                 nn.init.normal_(m.weight, 0, 0.01)
#                 if m.bias is not None:
#                         nn.init.constant_(m.bias, 0)

#     def forward(self, x, factor):
#         x = F.dropout(x, 0.3, self.training)
#         x = self.conv1(x)
#         x = self.relu(x)
#         x = F.dropout(x, 0.3, self.training)
#         x = self.conv2(x)
#         x = self.relu(x)
#         x = F.dropout(x, 0.3, self.training)
#         x = self.conv3(x)
#         x = self.relu(x)
#         x = self.conv4(x)
#         x = self.conv5(x)
#         x = x.mean(dim=-1)
#         x = self.tanh(x)
#         x = x*factor

#         return x

# class Unet_Decoder_Conv(nn.Module):
#     def __init__(self, pic1, pic2):
#         super().__init__()

#         self.out_conv1 = nn.Conv1d(encoder_decoder_channel_para[0], encoder_decoder_channel_para[0]*unet_decoder_conv_para[0], kernel_size=pic1*pic2, groups=encoder_decoder_channel_para[0])
#         self.out_batch1 = nn.BatchNorm1d(encoder_decoder_channel_para[0])
#         self.out_conv2 = nn.Conv1d(encoder_decoder_channel_para[0], encoder_decoder_channel_para[0]*unet_decoder_conv_para[1], kernel_size=unet_decoder_conv_para[0], groups=encoder_decoder_channel_para[0])
#         self.out_batch2 = nn.BatchNorm1d(encoder_decoder_channel_para[0])
#         self.out_conv3 = nn.Conv1d(encoder_decoder_channel_para[0], encoder_decoder_channel_para[0]
#         *unet_decoder_conv_para[2], kernel_size=unet_decoder_conv_para[1], groups=encoder_decoder_channel_para[0])
#         self.out_batch3 = nn.BatchNorm1d(encoder_decoder_channel_para[0])
#         self.out_conv4 = nn.Conv1d(encoder_decoder_channel_para[0], encoder_decoder_channel_para[0]*unet_decoder_conv_para[3], kernel_size=unet_decoder_conv_para[2], groups=encoder_decoder_channel_para[0])
#         self.out_relu = nn.ReLU()

#     def forward(self, output):
#         out_batch_size = output.shape[0]
#         out_channel_size = output.shape[1]

#         output = self.out_conv1(output)
#         output = output.view(out_batch_size, out_channel_size, unet_decoder_conv_para[0])
#         output = self.out_batch1(output)
#         output = self.out_relu(output)

#         output = self.out_conv2(output)
#         output = output.view(out_batch_size, out_channel_size, unet_decoder_conv_para[1])
#         output = self.out_batch2(output)
#         output = self.out_relu(output)

#         output = self.out_conv3(output)
#         output = output.view(out_batch_size, out_channel_size, unet_decoder_conv_para[2])
#         output = self.out_batch3(output)
#         output = self.out_relu(output)

#         output = self.out_conv4(output)
#         output = output.view(out_batch_size, out_channel_size, unet_decoder_conv_para[3])

#         return output

class UNet_Encoder(nn.Module):
    def __init__(self, in_channels):
        super().__init__()

        # begin
        self.begin_conv = nn.Conv2d(in_channels, in_channels, begin_end_conv_para[0], begin_end_conv_para[1], begin_end_conv_para[2])
        
        # left
        self.left_conv_1 = MutiConv(in_channels, encoder_decoder_channel_para[0])
        self.down_1 = nn.MaxPool2d(2, 2)

        self.left_conv_2 = MutiConv(encoder_decoder_channel_para[0], encoder_decoder_channel_para[1])
        self.down_2 = nn.MaxPool2d(2, 2)

        self.left_conv_3 = MutiConv(encoder_decoder_channel_para[1], encoder_decoder_channel_para[2])
        self.down_3 = nn.MaxPool2d(2, 2)

        self.initialize_weights()
       
    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # begin
        x = self.begin_conv(x)
        # print(x.shape)

        # left
        x1 = self.left_conv_1(x)
        x1_down = self.down_1(x1)

        x2 = self.left_conv_2(x1_down)
        x2_down = self.down_2(x2)

        x3 = self.left_conv_3(x2_down)
        x3_down = self.down_3(x3)

        return (x1, x2, x3, x3_down)
    

class UNet_Decoder(nn.Module):
    def __init__(self):
        super().__init__()

        # center
        self.center_conv = MutiConv(encoder_decoder_channel_para[2], encoder_decoder_channel_para[3])

        # right
        self.up_1 = nn.ConvTranspose2d(encoder_decoder_channel_para[3], encoder_decoder_channel_para[2], 2, 2)
        self.right_conv_1 = MutiConv(encoder_decoder_channel_para[3], encoder_decoder_channel_para[2])

        self.up_2 = nn.ConvTranspose2d(encoder_decoder_channel_para[2], encoder_decoder_channel_para[1], 2, 2)
        self.right_conv_2 = MutiConv(encoder_decoder_channel_para[2], encoder_decoder_channel_para[1])

        self.up_3 = nn.ConvTranspose2d(encoder_decoder_channel_para[1], encoder_decoder_channel_para[0], 2, 2)
        self.right_conv_3 = MutiConv(encoder_decoder_channel_para[1], encoder_decoder_channel_para[0])

        # output
        self.output = nn.ConvTranspose2d(encoder_decoder_channel_para[0], encoder_decoder_channel_para[0], begin_end_conv_para[0], begin_end_conv_para[1], begin_end_conv_para[2])
        self.output_batchnorm = nn.BatchNorm2d(encoder_decoder_channel_para[0])

        # self.unet_decoder_conv = Unet_Decoder_Conv(pic1, pic2)


        self.initialize_weights()
        
    def initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)

    def forward(self, x):

        x1, x2, x3, x3_down = x

        # center
        x4 = self.center_conv(x3_down)

        # right
        x5_up = self.up_1(x4)
        temp = torch.cat((x5_up, x3), dim=1)
        x5 = self.right_conv_1(temp)

        x6_up = self.up_2(x5)
        temp = torch.cat((x6_up, x2), dim=1)
        x6 = self.right_conv_2(temp)

        x7_up = self.up_3(x6)
        temp = torch.cat((x7_up, x1), dim=1)
        x7 = self.right_conv_3(temp)

        output = self.output(x7)
        output = self.output_batchnorm(output)
        
        # output
        output = torch.flatten(output, start_dim=1)

        # output = self.unet_decoder_conv(output)

        return output



class UNet_Encoder_Decoder(nn.Module):
    def __init__(self, in_channels, out_channels_velo, out_channels_depth, out_channels_thickness, pic1, pic2):
        super().__init__()

        # encoder
        self.encoder = UNet_Encoder(in_channels)
        self.encoder.initialize_weights()

        # decoder
        self.unet_decoder_flatten = UNet_Decoder()
        self.unet_decoder_flatten.initialize_weights()

        self.encoder_decoder_linear_depth = Encoder_Decoder_Linear(encoder_decoder_conv_para[0]*pic1*pic2,out_channels_depth)
        self.encoder_decoder_linear_depth.initialize_weights()

        self.encoder_decoder_linear_thickness = Encoder_Decoder_Linear(encoder_decoder_conv_para[0]*pic1*pic2,out_channels_thickness)
        self.encoder_decoder_linear_thickness.initialize_weights()

        self.encoder_decoder_linear_velocity = Encoder_Decoder_Linear(encoder_decoder_conv_para[0]*pic1*pic2,out_channels_velo)
        self.encoder_decoder_linear_velocity.initialize_weights()

    def forward(self, x):

        x = self.encoder(x)

        output_flatten = self.unet_decoder_flatten(x)

        output_depth = self.encoder_decoder_linear_depth(output_flatten)

        in_linear_thickness = output_depth + output_flatten
        output_thickness = self.encoder_decoder_linear_thickness(in_linear_thickness)

        in_linear_velocity = output_depth + output_thickness + output_flatten
        output_velocity = self.encoder_decoder_linear_velocity(in_linear_velocity)

        output = torch.cat([output_velocity, output_depth, output_thickness],dim=-1)


        return output

if __name__ == '__main__':

    model = UNet_Encoder_Decoder(2, 15, 1, 1, 41, 81)
    data = torch.rand(1, 2, 41, 81)
    out = model(data)
    print(out.shape)

