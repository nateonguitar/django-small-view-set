# Reasoning behind this library:

A note from the library creator:

I feel like a justification to not "just use DRF" is in order.

After working in Django Rest Framework for years, I liked how nice it was for getting an API up and running really quickly, but I hated how often I would get stuck debugging some abstracted thing in a serializer, or a viewset, then spend too much time implementing some niche (and usually hacky feeling) fix.

Sadly, there are a lot of these pain points in DRF, and a lack of separation-of-concerns. For instance, I always disliked how serializers don't just serialize, they do operations like creating and updating, often resulting in business logic in serializers. That is not serialization. When using mixins on DRF viewsets, often customization methods are required, like which permissions to use for each endpoint, which serializer to use, add a custom "perform_create" method to help serializers save (which is another separation-of-concerns issue, why is an endpoint router helping the serializer save?), etc. and it makes it difficult to do reverse lookups to endpoints. It also meant, while testing, POSTing to reverse('foo-list') to create, which really should be posting to the "foo-collection" or something else. It's nitpicky yes, but these nitpicks are all over.

So I wrote this. As little black-box as possible and a clear sepration of concerns. Surprisingly (because it was not the goal), I reduced the number of lines of code in every single one of my viewsets because I didn't need to register so many mixins, set up complex decorators, or define so many helper methods.

I still like some tools DRF provides, like throttles and serializers (when only used as validators or json generators), those are still completely compatible and honestly amazing.

This library also provides a pattern for creating a global exception-to-json-response handler, and it provides a default version you are welcome to copy from or use directly. I really liked my Spring Boot experience (and other frameworks) where the pattern is to throw any exception from anywhere, fail early, and a global exception handler will convert the errors to json responses.