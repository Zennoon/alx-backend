import { createClient, print } from 'redis';

const util = require('util');

function createRedisClient () {
  const client = createClient().on('connect', () => {
    console.log('Redis client connected to the server');
  }).on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
  });

  return client
}

const client = createRedisClient();

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
};

const displaySchoolValue = async (schoolName) => {
  const get = util.promisify(client.get);

  const val = await get(schoolName);
  console.log(val);
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
