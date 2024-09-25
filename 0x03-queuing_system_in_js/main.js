import { createQueue } from 'kue';
import createPushNotificationJobs from './8-job';

const queue = createQueue();

const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  }
];

createPushNotificationJobs(list, queue);
