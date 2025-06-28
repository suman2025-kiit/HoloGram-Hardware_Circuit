from model.hologram_model import HoloGramModel
import torch
import torch.nn as nn
import torch.optim as optim

model = HoloGramModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(50):
    depth = torch.rand(32, 256)  # Dummy depth input
    pose = torch.rand(32, 256)   # Dummy pose input
    target = torch.rand(32, 1)

    optimizer.zero_grad()
    output = model(depth, pose)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
torch.save(model.state_dict(), 'outputs/hologram_model.pth')