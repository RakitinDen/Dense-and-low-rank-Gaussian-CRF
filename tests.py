from layers import ConjugateGradients, dense_gaussian_crf

import torch
import torch.nn as nn
import torch.optim


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def optimization_test(n_epochs=10, shift=0.01):
    A = torch.normal(mean=0, std=0.1, size=(10, 128, 321 * 321), device=device, requires_grad=True)
    B = torch.normal(mean=0, std=0.1, size=(10, 321 * 321, 1), device=device, requires_grad=True)
    dcrf = dense_gaussian_crf(ConjugateGradients(shift))
    opt = torch.optim.Adam([A, B], lr=3e-2)
    criterion = nn.MSELoss()

    for i in range(n_epochs):
        opt.zero_grad()
        x = dcrf(A, B)
        loss = criterion(x, torch.zeros_like(x))
        loss.backward()
        print(loss)
        opt.step()

    x_opt = dcrf(A, B)
    return A, B, x_opt

optimization_test()
