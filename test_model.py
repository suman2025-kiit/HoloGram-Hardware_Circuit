from model.hologram_model import HoloGramModel
import torch

model = HoloGramModel()
model.load_state_dict(torch.load('outputs/hologram_model.pth'))
model.eval()

depth = torch.rand(1, 256)
pose = torch.rand(1, 256)

with torch.no_grad():
    output = model(depth, pose)
    print("Test Output:", output)