import express from 'express';
import { createQueue } from 'kue';
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();
const queue = createQueue();

const reserveSeat = function (number) {
  client.set('available_seats', number);
};

const getCurrentAvailableSeats = async function () {
  const get = promisify(client.get).bind(client);

  const val = await get('available_seats');
  return val;
};

const app = express();
let reservationEnabled = true;

app.get('/available_seats', (req, res) => {
  res.contentType = 'application/json';
  getCurrentAvailableSeats().then((seats) => {
    res.send({ numberOfAvailableSeats: seats });
  });
});

app.get('/reserve_seat', (req, res) => {
  res.contentType = 'application/json';
  if (!reservationEnabled) {
    res.send({ status: 'Reservation is blocked' });
  } else {
    const job = queue.create('reserve_seat').save((err) => {
      if (!err) {
        res.send({ status: 'Reservation in process' });
      }
    });

    job.on('complete', () => {
      console.log(`Seat reservation job #${job.id} completed`);
    });

    job.on('failed', (err) => {
      console.log(`Seat reservation job #${job.id} failed: ${err}`);
    });
  }
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', function (job, done) {
    getCurrentAvailableSeats().then((seats) => {
      reserveSeat(seats - 1);
      if (seats - 1 >= 0) {
        reservationEnabled = !!((seats - 1));
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    });
  });
  res.contentType = 'application/json';
  res.send({ status: 'Queue processing' });
});

app.listen(1245, () => {
  reserveSeat(50);
});
