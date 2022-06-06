const Koa = require('koa');
const { createServer } = require('http');
const Router = require('koa-router');
const cors = require('@koa/cors');
const logger = require('koa-logger');
const { Server } = require('socket.io');

const PORT = 4000;

const app = new Koa();
const server = createServer(app.callback);
const io = new Server(server, { cors: { origin: 'http://localhost:3000' } });
const router = new Router();

app.use(logger());
app.use(cors());

router.post('/detect/:object', async (ctx, next) => {
  const { object } = ctx.params;
  ctx.status = 200;
});

app.use(router.routes());
app.use(async (ctx) => {
  ctx.status = 404;
});

io.on('connection', (socket) => {
  console.log(`Client connected: id=${socket.id}`);
});

server.listen(PORT, () => {
  console.log('Server started');
});
