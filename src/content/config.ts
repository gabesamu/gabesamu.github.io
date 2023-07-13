// 1. Import utilities from `astro:content`
import { z, defineCollection } from 'astro:content';
// 2. Define your collection(s)
const articleCollection = defineCollection({
    type: "content",
    schema: z.object({
        title: z.string(),
        pubDate: z.date(),
        description: z.string(),
        tags: z.array(z.string()),
    })
 });


// const literalSchema = z.union([z.string(), z.number(), z.boolean(), z.null()]);
// type Literal = z.infer<typeof literalSchema>;
// type Json = Literal | { [key: string]: Json } | Json[];
// const jsonSchema: z.ZodType<Json> = z.lazy(() =>
// z.union([literalSchema, z.array(jsonSchema), z.record(jsonSchema)])
// );


 const noteCollection = defineCollection({
    type: "data",
    schema: z.object({
        source_title: z.string(),
        pubDate: z.coerce.date(),
        author: z.string(),
        text: z.string(),
        note: z.string(),
        tags: z.array(z.string()),
        url: z.nullable(z.string()),
        is_discard: z.boolean(),
    }),

 });
// 3. Export a single `collections` object to register your collection(s)
//    This key should match your collection directory name in "src/content"
export const collections = {
  "articles": articleCollection,
  "notes": noteCollection,
};
