import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient().on('connect', () => {
  console.log('Redis client connected to the server');
}).on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
};

const displaySchoolValue = async (schoolName) => {
  const get = promisify(client.get).bind(client);

  const val = await get(schoolName);
  console.log(val);
};

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', 100);
displaySchoolValue('HolbertonSanFrancisco');
