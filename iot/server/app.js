const Koa = require('koa');
const http = require('http');
const Router = require('koa-router');
const logger = require('koa-logger');
const io = require('socket.io');

const PORT = 4000;

const app = new Koa();
const server = http.createServer(app.callback());
const router = new Router();

app.use(logger());

router.post('/detect/:object', async (ctx, next) => {
  const { object } = ctx.params;
  ctx.status = 200;
});

app.use(router.routes());
app.use(async (ctx) => {
  ctx.status = 404;
});

server.listen(PORT, () => {
  console.log('Server started');
});

io(server).on('connect', (socket) => {
  console.log(`Client connected: id=${socket.id}`);
});
