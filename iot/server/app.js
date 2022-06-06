const Koa = require('koa');
const { createServer } = require('http');
const Router = require('koa-router');
const cors = require('@koa/cors');
const logger = require('koa-logger');
const { Server } = require('socket.io');

const app = new Koa();
const server = createServer(app.callback());
const io = new Server(server, { cors: { origin: 'http://localhost:3000' } });
const router = new Router();

const PORT = 4000;
let client = undefined;

app.use(logger());
app.use(cors());

router.post('/detect/:object', async (ctx) => {
  const { object } = ctx.params;

  if (client !== undefined) client.emit('detect', object);

  ctx.status = 200;
});

router.all('/', async (ctx) => {
  ctx.status = 404;
});

app.use(router.routes()).use(router.allowedMethods());

io.on('connection', (socket) => {
  console.log(`Client connected: id=${socket.id}`);
  client = socket;
});

server.listen(PORT, () => {
  console.log('Server started');
});
