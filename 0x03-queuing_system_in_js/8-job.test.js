import { describe, it, before, after, afterEach } from 'mocha';
import { createQueue } from 'kue';
import { expect } from 'chai';
import createPushNotificationJobs from './8-job';

const queue = createQueue();

describe('createPushNotificationJobs', function () {
  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('display an error message if jobs is not an array', function () {
    expect(createPushNotificationJobs.bind(this, 'Invalid', queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', function () {
    createPushNotificationJobs([
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4321 to verify your account'
      }
    ], queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
  });
});
