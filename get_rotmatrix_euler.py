import numpy as np
import torch
import torch.nn as nn

tform1 = np.array([[[0, -1.0000, 0],
                    [1.0000, 0, 0],
                    [0,0, 1.0000]],

                   [[0, 1.0000, 0],
                    [-1.0000, 0, 0],
                    [0,0, 1.0000]]])

class Rotation3D(nn.Module):
    def __init__(self, number=None):
        super(Rotation3D, self).__init__()

        # Number of output of the localization network (Expected image is frames, number of features)
        self.phi = torch.nn.Parameter(torch.tensor([0.0]).view(1,1))
        self.theta = torch.nn.Parameter(torch.tensor([0.0]).view(1,1))
        self.psi = torch.nn.Parameter(torch.tensor([0.0]).view(1,1))

    def forward(self):
        rot = torch.zeros(3, 3, device=self.phi.device)
        rot[0, 0] = torch.cos(self.theta) * torch.cos(self.psi)
        rot[0, 1] = -torch.cos(self.phi) * torch.sin(self.psi) + torch.sin(self.phi) * torch.sin(self.theta) * torch.cos(self.psi)
        rot[0, 2] =  torch.sin(self.phi) * torch.sin(self.psi) + torch.cos(self.phi) * torch.sin( self.theta) * torch.cos(self.psi)

        rot[1, 0] = torch.cos(self.theta)*torch.sin(self.psi)
        rot[1, 1] = torch.cos(self.phi) * torch.cos(self.psi) + torch.sin(self.phi) * torch.sin( self.theta) * torch.sin(self.psi)
        rot[1, 2] = -torch.sin(self.phi) * torch.cos(self.psi) + torch.cos(self.phi) * torch.sin(self.theta) * torch.sin( self.psi)

        rot[2, 0] = -torch.sin(self.theta)
        rot[2, 1] = torch.sin( self.phi) * torch.cos( self.theta)
        rot[2, 2] = torch.cos( self.phi ) * torch.cos( self.theta)

        return rot
def average_rotation( r=None):
    r"""Finds a rotation to a common space

    Args:
        r (array): a 3D array [Nt x 3 x 3] containing rotation matrices over time
    Returns:
        rp (array): a 3D array [Nt x 3 x 3] containing corrected rotation matrices
    """

    # This just defines a rotation matrix using euler angles
    RotModel = Rotation3D()

    # Optimize using Adam
    optimizer = torch.optim.Adam(RotModel.parameters(), lr=1e-4)

    # Need identify to get loss
    id = torch.eye(3)

    # Get the rotation matrix
    R = torch.tensor(r)
    print(R)
    print(R.shape)
    for epoch in range(100000):

        optimizer.zero_grad()

        # B is the correction to R
        B = RotModel()
        B= B.double()
        R = R.double()
        # Calculate the corrected matrix
        y = torch.matmul(B, R)

        # Loss is average difference from identity
        loss = torch.sum(torch.abs(y - id) ** 2)

        if epoch % 1000 == 0:
            print(f'Epoch {epoch} Loss = {loss.item()}')

        loss.backward()
        optimizer.step()

    # Apply rotation to R
    B = RotModel()

    print(f'Inverse Common Rotation')
    print(f'  Psi={RotModel.psi[0,0]} ')
    print(f'  Theta={RotModel.theta[0, 0]} ')
    print(f'  Phi={RotModel.phi[0, 0]} ')
    print(f'  B = {B}')

    return(B.detach().cpu().numpy())

average_rotation(tform1)
