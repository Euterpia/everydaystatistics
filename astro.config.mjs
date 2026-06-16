// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://everydaystatistics.com',
  output: 'static',
  integrations: [
    sitemap({
      // /subscribed is a noindex post-signup confirmation page; keep it out of the sitemap.
      filter: (page) => !page.includes('/subscribed'),
      // Static site rebuilt and redeployed as a whole; stamp the build date as lastmod.
      serialize(item) {
        item.lastmod = new Date().toISOString();
        return item;
      },
    }),
  ],
});
