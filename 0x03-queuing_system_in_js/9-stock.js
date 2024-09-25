import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();

const reserveStockById = function (itemId, stock) {
  client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async function (itemId) {
  const get = promisify(client.get).bind(client);

  const val = await get(`item.${itemId}`);
  return val;
};

const listProducts = [
  {
    id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4
  },
  {
    id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5
  }
];

for (const product of listProducts) {
  reserveStockById(product.id, product.stock);
}

const getItemById = function (id) {
  return listProducts.filter((product) => product.id === id)[0];
};

const app = express();

app.get('/list_products', (req, res) => {
  res.contentType = 'application/json';
  res.send(listProducts.map((product) => {
    const jsonRepr = {
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock
    };
    return jsonRepr;
  }));
});

app.get('/list_products/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  res.contentType = 'application/json';

  if (!item) {
    res.send({ status: 'Product not found' });
  } else {
    getCurrentReservedStockById(itemId).then((stock) => {
      res.send({
        itemId: item.id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock,
        currentQuantity: parseInt(stock)
      });
    });
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  res.contentType = 'application/json';

  if (!item) {
    res.send({ status: 'Product not found' });
  } else {
    getCurrentReservedStockById(itemId).then((stock) => {
      if (!parseInt(stock)) {
        res.send({ status: 'Not enough stock available', itemId });
      } else {
        reserveStockById(itemId, stock - 1);
        res.send({ status: 'Reservation confirmed', itemId });
      }
    });
  }
});

app.listen(1245);
