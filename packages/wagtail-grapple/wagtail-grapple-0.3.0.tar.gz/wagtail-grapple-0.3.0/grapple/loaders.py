from promise import Promise
from functools import partial
from promise.dataloader import DataLoader


class GenericModelLoader(DataLoader):
    model = None
    all_results_loaded = False

    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

    def batch_load_fn(self, keys):
        # Effieciently query database
        items = {item.id: item for item in self.model.objects.filter(id__in=keys)}

        # Return matching elemenrs,
        return Promise.resolve([items.get(item_id) for item_id in keys])

    # Equivelent to Model.objects.all() but dataloaded...
    def load_all(self, resolve_queryset=None):
        # type: (Hashable) -> Promise
        """
        Equivelent to Model.objects.all() but results are batched into Dataloader.
        """
        # If caching and there is a cache-hit, return all cached Promises.
        if self.cache:
            cached_keys = self._promise_cache.keys()
            if self.all_results_loaded:
                return self.load_many(cached_keys)

        # Otherwise, produce a Promise for each db result.
        promises = []
        queryset = lambda: self.model.objects.all()
        if resolve_queryset:
            queryset = resolve_queryset

        for result in queryset():
            cache_key = self.get_cache_key(result.id)
            promise = Promise.resolve(result)
            promises.append(promise)
            if self.cache:
                self._promise_cache[cache_key] = promise

        # Return all the models.
        self.all_results_loaded = True
        return Promise.all(promises)


# Return a model loader than binds to a loaders store (should be attached to Request object).
def create_model_loader(loaders):
    def model_loader(model):
        # Check if already created a loader for that model
        existing_loader = loaders.get(model, None)
        if existing_loader is not None:
            return existing_loader

        # Else create, save and return one.
        loaders[model] = GenericModelLoader(model)
        return loaders[model]

    return model_loader
