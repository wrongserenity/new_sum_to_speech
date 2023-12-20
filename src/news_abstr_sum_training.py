from transformers import T5ForConditionalGeneration, T5Tokenizer, T5Config
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from bert_score import score
import torch

from datasets import load_dataset

RUN_COUNT = 10
RUN_DATASET_SIZE = 1000
START_MODEL_NAME = "result_3"  # "cointegrated/rut5-base"
MODEL_SAVE_PATH = "../result/models_abs_sum/"


class CustomDataset(Dataset):
    def __init__(self, tokenized_data, labels_):
        self.input_ids = tokenized_data['input_ids']
        self.attention_mask = tokenized_data['attention_mask']
        self.labels = labels_

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_mask[idx], 'labels': self.labels[idx]}


if __name__ == "__main__":
    model_name = START_MODEL_NAME
    dataset = load_dataset('IlyaGusev/gazeta', revision="v2.0")
    dataset_size = RUN_DATASET_SIZE
    train_size = int(0.8 * dataset_size)

    for i in range(RUN_COUNT):
        # ----------------------------- Prepare -----------------------------
        train_start = i * int(2*dataset_size / 3)
        train_end = train_start + train_size

        test_start = train_end
        test_end = train_start + dataset_size

        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        train_dataset, test_dataset = dataset['train'][train_start:train_end], dataset['train'][test_start:test_end]
        train_tokenized_data = tokenizer(train_dataset['text'], truncation=True, padding=True, return_tensors='pt', max_length=512)
        labels_tokenized_data = tokenizer(train_dataset['summary'], truncation=True, padding=True, return_tensors='pt',max_length=150)

        train_dataset = CustomDataset(train_tokenized_data, labels_tokenized_data['input_ids'])
        train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True)

        # ----------------------------- Train -----------------------------
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 'cpu'
        model.to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

        num_epochs = 3
        for epoch in range(num_epochs):
            model.train()
            for batch in tqdm(train_dataloader, desc=f'Epoch {epoch + 1}/{num_epochs}'):
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # ----------------------------- Save Model -----------------------------
        save_path = MODEL_SAVE_PATH + "result_fourth_" + str(i)
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)

        # ----------------------------- Calc BERTscore -----------------------------
        test_tokenized_data = tokenizer(test_dataset['text'], truncation=True, padding=True, return_tensors='pt', max_length=512)
        labels_tokenized_data_test = tokenizer(test_dataset['summary'], truncation=True, padding=True, return_tensors='pt', max_length=150)

        test_dataset = CustomDataset(test_tokenized_data, labels_tokenized_data_test['input_ids'])
        test_dataloader = DataLoader(test_dataset, batch_size=2, shuffle=False)

        model.eval()
        predictions = []
        references = []
        for batch in tqdm(test_dataloader, desc='Evaluating on test set'):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            with torch.no_grad():
                generated_ids = model.generate(input_ids, attention_mask=attention_mask, max_length=150)

            generated_texts = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
            target_texts = tokenizer.batch_decode(labels, skip_special_tokens=True)

            predictions.extend(generated_texts)
            references.extend(target_texts)

        P, R, F1 = score(predictions, references, lang="ru")
        print(f"{i} BERTscore: Precision={P.mean():.4f}, Recall={R.mean():.4f}, F1={F1.mean():.4f}")

        # ----------------------------- Prepare Next Run -----------------------------
        model_name = save_path
