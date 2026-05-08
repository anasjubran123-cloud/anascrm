import { defineCollection, z } from 'astro:content';

// Content collections set up minimally for Phase 1. Real schemas land in
// Phase 5 alongside placeholder tracking in CONTENT.md. Each collection is
// defined now so adding entries in later phases requires no scaffolding work.

const localeEnum = z.enum(['en', 'ar']);

const capabilities = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    locale: localeEnum,
    summary: z.string(),
    order: z.number().default(0),
    draft: z.boolean().default(true),
  }),
});

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    locale: localeEnum,
    sector: z.string().optional(),
    summary: z.string(),
    approved: z.boolean().default(false),
    placeholder: z.boolean().default(true),
    order: z.number().default(0),
  }),
});

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    locale: localeEnum,
    publishedAt: z.coerce.date(),
    summary: z.string(),
    draft: z.boolean().default(true),
  }),
});

const careers = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    locale: localeEnum,
    location: z.string().default('Al Khobar, Saudi Arabia'),
    type: z.enum(['full-time', 'part-time', 'contract', 'internship']).default('full-time'),
    summary: z.string(),
    open: z.boolean().default(true),
  }),
});

const partners = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    href: z.string().url().optional(),
    // Display approval — partner logos must not appear publicly without a
    // recorded "yes" here. Site stays offline during dev, so v1 ships with
    // approved: false and the launch checklist reconciles this before public
    // launch.
    approved: z.boolean().default(false),
    note: z.string().optional(),
  }),
});

export const collections = {
  capabilities,
  projects,
  news,
  careers,
  partners,
};
