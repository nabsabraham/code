# Domain-driven-design:
* Two important concepts are `Entities` and `Value` objects
* deciding whether a concept is an Entity or a Value object is not straightforward because depending on the domain, they may change
* for example, the concept `money` when we're talking about people and their bank accounts is immutable and doens't have an id. IE, if nabila has 5 dollars today and a different 5 dollars tomorrow, the amount of money nabila has is **still 5 dollars** 
* but, if we're like the government tracking the statistics of a dollar bill, then my 5$ bill is an `Entity` because it has an id to it and its properties are mutable like, who owns this bill at the moment 

## Entities:
* Entities have `identity equality` and we make this explicit in code with an equality check in the object: 
    ```
    class Batch:
        # reference = the identity id 

        def __eq__(self, other):
            if not isinstance(other, Batch):
                return False
            return other.reference == self.reference
    ```
* the `__eq__` magic method is executed when you check equality in python
* the `__hash__` method is another magic method thta controls the behavior of objects when you add them to sets or use them as dict keys 

## Values: 
* Value objects hold business concepts that have data but no identity 
    * Recall the example that an Order can have multiple OrderLines but just pointing a Line back to the order is not enough to uniquely identify it
    * Value objects just hold values, if we have a Money object: 
    ```
    class Money(NamedTuple):
        currency: str
        value: int
    ```
    * it doesn't matter if we define `Money('usd', 10)` more than once because 10$ is 10$
    * A `Value` object is on that is **only** identified by its own data. If its own data changes, it's a new `Value` object.

## In summary :
* taken from [here](https://enterprisecraftsmanship.com/posts/entity-vs-value-object-the-ultimate-list-of-differences/)
* Entities have their own intrinsic identity, value objects don’t.
* The notion of identity equality refers to entities; the notion of structural equality refers to value objects; the notion of reference equality refers to both.
    * btw, structural equality means you compare two objects and for them to be equal, all tehir members must have the same values
    * identity equality means two objects must be equal if their `id` attribute is the same 
* Entities have a history; value objects have a zero lifespan.
* A value object should always belong to one or several entities, it can’t live by its own.
* Value objects should be immutable; entities are almost always mutable.
* To recognize a value object in your domain model, mentally replace it with an integer.
* Value objects shouldn’t have their own tables in the database.
* Always prefer value objects over entities in your domain model.

# In Python
* when creating value objects, should make sure all attributes are immutable and that the object's hash is based on all value attributes
* the second point is important so you can compare two value objects
* you get both for free using `@dataclass` and `frozen=True`