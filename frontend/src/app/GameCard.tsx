type GameCardProps = {
  id: number
  title: string
  rating?: number | null
  imageUrl?: string | null
  releaseDate?: string | null
  rawgUrl?: string | null
  onResolveRawgUrl?: () => Promise<string | null>
  onImport?: (id: number) => void
  onRemove?: (title: string) => void
}

export default function GameCard({
  id,
  title,
  rating,
  imageUrl,
  releaseDate,
  rawgUrl,
  onResolveRawgUrl,
  onImport,
  onRemove,
}: GameCardProps) {
  const displayRating =
    rating === null || rating === undefined ? "N/A" : rating.toFixed(1)
  const showRemove = Boolean(onRemove)
  const showImport = Boolean(onImport) && !showRemove
  const handleOpen = async () => {
    const url = rawgUrl ?? (onResolveRawgUrl ? await onResolveRawgUrl() : null)
    if (!url) {
      return
    }
    window.open(url, "_blank", "noopener,noreferrer")
  }
  const isClickable = Boolean(rawgUrl || onResolveRawgUrl)

  return (
    <div
      className={`flex w-full items-center gap-4 rounded-2xl border border-zinc-200 bg-gradient-to-br from-white via-zinc-50 to-zinc-100 p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-zinc-800 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900 ${isClickable ? "cursor-pointer" : ""}`}
      onClick={isClickable ? () => void handleOpen() : undefined}
      role={isClickable ? "link" : undefined}
      tabIndex={isClickable ? 0 : -1}
      onKeyDown={(event) => {
        if (isClickable && (event.key === "Enter" || event.key === " ")) {
          event.preventDefault()
          void handleOpen()
        }
      }}
    >
      <div className="relative h-20 w-14 flex-shrink-0 overflow-hidden rounded-lg bg-gradient-to-br from-zinc-200 to-zinc-100 dark:from-zinc-800 dark:to-zinc-700">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={`${title} cover`}
            className="h-full w-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-xs font-medium text-zinc-500 dark:text-zinc-300">
            No Image
          </div>
        )}
      </div>

      <div className="flex w-full items-center justify-between gap-4">
        <div className="flex flex-col gap-1">
          {rawgUrl ? (
            <a
              href={rawgUrl}
              target="_blank"
              rel="noreferrer"
              className="text-base font-semibold text-zinc-900 transition hover:text-zinc-700 dark:text-zinc-50 dark:hover:text-zinc-200"
            >
              {title}
            </a>
          ) : (
            <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-50">
              {title}
            </h2>
          )}
          <div className="flex flex-wrap items-center gap-2 text-xs text-zinc-600 dark:text-zinc-300">
            <span className="rounded-full bg-zinc-200 px-2 py-0.5 font-semibold text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
              Rating {displayRating}
            </span>
            {releaseDate && (
              <span className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700">
                {releaseDate}
              </span>
            )}
          </div>
        </div>

        {showImport && onImport && (
          <button
            onClick={(event) => {
              event.stopPropagation()
              onImport(id)
            }}
            className="rounded-full bg-zinc-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-black dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-white"
          >
            Add to Library
          </button>
        )}
        {showRemove && onRemove && (
          <button
            onClick={(event) => {
              event.stopPropagation()
              onRemove(title)
            }}
            className="rounded-full border border-zinc-300 px-4 py-2 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
          >
            Remove from Library
          </button>
        )}
      </div>
    </div>
  )
}
