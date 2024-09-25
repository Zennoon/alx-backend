import { createQueue } from 'kue';

const queue = createQueue();

const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account'
};

const pushJob = queue.create('push_notification_code', jobData).save((err) => {
  if (!err) {
    console.log(`Notification job created: ${pushJob.id}`);
  }
});

pushJob.on('complete', () => {
  console.log('Notification job completed');
});

pushJob.on('failed', () => {
  console.log('Notification job failed');
});
