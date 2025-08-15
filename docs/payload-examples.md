# Exemplos de Payload para Testes

## 1. Smartphones

### Criar Smartphone 1
```json
{
    "name": "iPhone 15 Pro",
    "image_url": "https://example.com/iphone15pro.jpg",
    "description": "O iPhone mais avançado com chip A17 Pro",
    "price": 9499.00,
    "rating": 4.8,
    "specifications": {
        "tela": "6.1 polegadas OLED",
        "processador": "A17 Pro",
        "armazenamento": "256GB",
        "ram": "8GB",
        "camera": "48MP + 12MP + 12MP",
        "bateria": "3274 mAh",
        "sistema": "iOS 17",
        "cor": "Titânio Natural"
    }
}
```

### Criar Smartphone 2
```json
{
    "name": "Samsung Galaxy S24 Ultra",
    "image_url": "https://example.com/s24ultra.jpg",
    "description": "O Galaxy mais poderoso com IA integrada",
    "price": 9799.00,
    "rating": 4.7,
    "specifications": {
        "tela": "6.8 polegadas Dynamic AMOLED",
        "processador": "Snapdragon 8 Gen 3",
        "armazenamento": "256GB",
        "ram": "12GB",
        "camera": "200MP + 12MP + 50MP + 10MP",
        "bateria": "5000 mAh",
        "sistema": "Android 14",
        "cor": "Titanium Black"
    }
}
```

### Criar Smartphone 3
```json
{
    "name": "Google Pixel 8 Pro",
    "image_url": "https://example.com/pixel8pro.jpg",
    "description": "O melhor do Android com IA do Google",
    "price": 8999.00,
    "rating": 4.6,
    "specifications": {
        "tela": "6.7 polegadas LTPO OLED",
        "processador": "Google Tensor G3",
        "armazenamento": "256GB",
        "ram": "12GB",
        "camera": "50MP + 48MP + 48MP",
        "bateria": "5050 mAh",
        "sistema": "Android 14",
        "cor": "Obsidian"
    }
}
```

## 2. Notebooks

### Criar Notebook 1
```json
{
    "name": "MacBook Pro 14",
    "image_url": "https://example.com/macbook14.jpg",
    "description": "MacBook Pro com chip M3 Pro",
    "price": 14999.00,
    "rating": 4.9,
    "specifications": {
        "processador": "Apple M3 Pro",
        "memoria": "32GB RAM",
        "armazenamento": "512GB SSD",
        "tela": "14.2 polegadas Liquid Retina XDR",
        "gpu": "GPU 18-core",
        "sistema": "macOS Sonoma",
        "bateria": "22 horas",
        "peso": "1.55 kg"
    }
}
```

### Criar Notebook 2
```json
{
    "name": "Dell XPS 13 Plus",
    "image_url": "https://example.com/xps13plus.jpg",
    "description": "Ultrabook premium com Intel Core de 13ª geração",
    "price": 12499.00,
    "rating": 4.7,
    "specifications": {
        "processador": "Intel Core i7-1360P",
        "memoria": "16GB RAM LPDDR5",
        "armazenamento": "512GB NVMe SSD",
        "tela": "13.4 polegadas 4K Touch",
        "gpu": "Intel Iris Xe",
        "sistema": "Windows 11 Pro",
        "bateria": "12 horas",
        "peso": "1.26 kg"
    }
}
```

### Criar Notebook 3
```json
{
    "name": "Lenovo ThinkPad X1 Carbon",
    "image_url": "https://example.com/x1carbon.jpg",
    "description": "Notebook empresarial leve e potente",
    "price": 11999.00,
    "rating": 4.6,
    "specifications": {
        "processador": "Intel Core i5-1340P",
        "memoria": "16GB RAM",
        "armazenamento": "256GB SSD",
        "tela": "14 polegadas WUXGA",
        "gpu": "Intel Iris Xe",
        "sistema": "Windows 11 Pro",
        "bateria": "15 horas",
        "peso": "1.12 kg"
    }
}
```

## 3. Smartwatches

### Criar Smartwatch 1
```json
{
    "name": "Apple Watch Series 9",
    "image_url": "https://example.com/watch9.jpg",
    "description": "O smartwatch mais avançado da Apple",
    "price": 4999.00,
    "rating": 4.8,
    "specifications": {
        "tela": "1.9 polegadas Retina LTPO OLED",
        "processador": "S9 SiP",
        "armazenamento": "64GB",
        "sensores": "Cardíaco, ECG, Oxímetro",
        "bateria": "18 horas",
        "material": "Alumínio",
        "resistencia": "WR50",
        "conectividade": "GPS + Cellular"
    }
}
```

### Criar Smartwatch 2
```json
{
    "name": "Samsung Galaxy Watch 6 Pro",
    "image_url": "https://example.com/watch6pro.jpg",
    "description": "Smartwatch premium com WearOS",
    "price": 3999.00,
    "rating": 4.6,
    "specifications": {
        "tela": "1.4 polegadas Super AMOLED",
        "processador": "Exynos W920",
        "armazenamento": "16GB",
        "sensores": "BioActive, ECG, Pressão",
        "bateria": "590mAh",
        "material": "Titânio",
        "resistencia": "5ATM + IP68",
        "conectividade": "GPS + LTE"
    }
}
```

### Criar Smartwatch 3
```json
{
    "name": "Garmin Fenix 7X Solar",
    "image_url": "https://example.com/fenix7x.jpg",
    "description": "Relógio GPS multiesporte premium",
    "price": 7499.00,
    "rating": 4.9,
    "specifications": {
        "tela": "1.4 polegadas MIP",
        "processador": "NXP i.MX 6",
        "armazenamento": "32GB",
        "sensores": "GPS Multi-banda, Cardíaco, Altímetro",
        "bateria": "37 dias (modo smartwatch)",
        "material": "Titânio com DLC",
        "resistencia": "10ATM",
        "conectividade": "GPS + GLONASS + Galileo"
    }
}
```

## Exemplos de Requisições

### 1. Criar um item
```bash
curl -X POST http://localhost:8080/items \
  -H "Content-Type: application/json" \
  -d @payload.json
```

### 2. Comparar itens (após criar)
```bash
curl -X GET "http://localhost:8080/items/compare?ids=1,2,3"
```

### 3. Atualizar um item
```bash
curl -X PATCH http://localhost:8080/items/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 8999.00, "rating": 4.7}'
```
