SELECT
	collections.id,
	collections.name,
	MostRecentCap.image_thumbnail,
	CollectionSizes.count,
	auth_user.username AS owner_username
FROM public.collectionsapp_collection collections
INNER JOIN (
	SELECT
		a.collection_id,
		a.image_thumbnail,
		a.created
	FROM public.collectionsapp_bottlecap a
	LEFT JOIN public.collectionsapp_bottlecap b ON
		a.collection_id = b.collection_id AND
		a.created < b.created
	WHERE b.id IS NULL
) MostRecentCap ON collections.id = MostRecentCap.collection_id
LEFT JOIN (
	SELECT
		collection_id,
		count(*) AS count
	FROM public.collectionsapp_bottlecap
	GROUP BY collection_id
) CollectionSizes ON collections.id = CollectionSizes.collection_id
LEFT JOIN auth_user ON collections.owner_id = auth_user.id
ORDER BY MostRecentCap.created DESC