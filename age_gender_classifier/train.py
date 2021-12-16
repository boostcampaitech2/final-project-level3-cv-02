import torch
import torch.nn as nn
from model import Net
from dataloader import AAFDDataLoader
from tqdm import tqdm

def train(model, criterion, optimizer, epochs):
    train_loader, val_loader = AAFDDataLoader(mode="train"), AAFDDataLoader(mode="val")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device is {}".format(device))
    model = model.to(device)
 
    best_loss = 1e10
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        val_loss = 0
        total = 0
        correct = 0

        for i, (x, y) in enumerate(tqdm(train_loader)):
            x = x.to(device)
            y = y.to(device)

            optimizer.zero_grad()
            y_ = model.forward(x)

            loss = criterion(y_, y)
            loss.backward()
            optimizer.step()

            train_loss += loss.cpu().detach().numpy()

        train_loss /= len(train_loader)

        model.eval()
        with torch.no_grad():
            for x, y in val_loader:
                x = x.to(device)
                y = y.to(device)
                y_ = model.forward(x)
                
                loss = criterion(y_, y)
                val_loss += loss.cpu().detach().numpy()

                preds = y_.argmax(dim=1)
                total += y.size(0)
                correct += (preds == y).sum().item()
            val_acc = correct / total * 100
            val_loss /= len(val_loader)

        print("Epoch [{}/{}] train_loss: {:.3f}, val_loss: {:.3f}, val_acc: {:.2f}".format(
            epoch+1, epochs, train_loss, val_loss, val_acc
        ))   

        if best_loss > val_loss:
            best_loss = val_loss
            print("update best model")
            torch.save(model.state_dict(), "./checkpoints/best.pt")
        torch.save(model.state_dict(), "./checkpoints/last.pt")

def main():
    model = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    epochs = 50
    train(model, criterion, optimizer, epochs=epochs)

main()