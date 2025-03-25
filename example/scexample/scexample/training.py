# number of epochs to train the model
from pathlib import Path
from typing import Any
import numpy as np
from pydantic import BaseModel
from scexample.data import DataLoaders
import torch
import torch.nn as nn
from torch.optim import Optimizer


class TrainingModel(BaseModel):
    model: nn.Module
    optimizer: Optimizer
    criterion: Any

    model_config = {"arbitrary_types_allowed": True}

    def train_step(self, data, target):

        # clear the gradients of all optimized variables
        self.optimizer.zero_grad()
        # forward pass: compute predicted outputs by passing inputs to the model
        output = self.model(data)
        # calculate the loss
        loss = self.criterion(output, target)
        # backward pass: compute gradient of the loss with respect to model parameters
        loss.backward()
        # perform a single optimization step (parameter update)
        self.optimizer.step()
        # update running training loss
        return loss.item()


    def validation_step(self, data, target):
        # forward pass: compute predicted outputs by passing inputs to the model
        output = self.model(data)
        # calculate the loss
        loss = self.criterion(output, target)
        # update running validation loss
        return loss.item()

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

class Trainer(BaseModel):
    dataloaders: DataLoaders
    training_model: TrainingModel
    n_epochs: int
    output_folder: Path

    model_config = {"arbitrary_types_allowed": True}

    def train(self):
        valid_loss_min = np.inf

        for epoch in range(self.n_epochs):
            train_loss = 0.0
            valid_loss = 0.0

            self.training_model.train()
            for data, target in iter(self.dataloaders.train):
                train_loss += self.training_model.train_step(data, target)

            self.training_model.eval()
            for data, target in iter(self.dataloaders.valid):
                valid_loss += self.training_model.validation_step(data, target)

            train_loss = train_loss / len(self.dataloaders.train)
            valid_loss = valid_loss / len(self.dataloaders.valid)

            print(
                "Epoch: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}".format(
                    epoch + 1, train_loss, valid_loss
                )
            )

            if valid_loss <= valid_loss_min:
                print(
                    "Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...".format(
                        valid_loss_min, valid_loss
                    )
                )
                self.save(self.output_folder / "model.pt")   
                valid_loss_min = valid_loss


    def save(self, model_output_path):
        torch.save(self.training_model.model.state_dict(), model_output_path)