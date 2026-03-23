import mitt from 'mitt';

type AppEvents = {
  login: void;
  logout: void;
};

const eventBus = mitt<AppEvents>();

export default eventBus;
