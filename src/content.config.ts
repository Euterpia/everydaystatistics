import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const units = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/units' }),
  schema: z.object({
    title: z.string(),
    unitId: z.string(),
    area: z.number(),
    areaName: z.string(),
    areaSlug: z.string(),
    tier: z.number().optional(),
    prerequisites: z.array(z.string()).default([]),
    summary: z.string(),
    duration: z.number().default(15),
    bayesEncounter: z.number().optional(),
    draft: z.boolean().default(true),
  }),
});

export const collections = { units };
