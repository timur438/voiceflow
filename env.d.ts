/// <reference types="vite/client" />

declare module "*.vue" {
  import { DefineComponent } from 'vue';
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  const component: DefineComponent<{}, {}, unknown>;
  export default component;
}

declare module "crypto-js" {
  import CryptoJS from "crypto-js";
  export = CryptoJS;
}