"use client"

import { useEffect, useMemo, useState } from "react"

type GameCardProps = {
  id: number
  title: string
  rating?: number | null
  personalRating?: number | null
  playState?: string | null
  platform?: string | null
  imageUrl?: string | null
  releaseDate?: string | null
  rawgUrl?: string | null
  rawgPlatforms?: string[] | null
  tags?: string[]
  notesPreview?: string | null
  favorite?: boolean
  showSelect?: boolean
  isSelected?: boolean
  onResolveRawgUrl?: () => Promise<string | null>
  onImport?: (id: number) => void
  onRemove?: (title: string) => void
  onToggleSelect?: (id: number, selected: boolean) => void
  onToggleFavorite?: (id: number, next: boolean) => void
  onOpenDetails?: (id: number) => void
  onUpdate?: (
    id: number,
    update: { personal_rating?: number | null; platform?: string | null },
  ) => Promise<void> | void
  layout?: "list" | "grid"
}

export default function GameCard({
  id,
  title,
  rating,
  personalRating,
  playState,
  platform,
  imageUrl,
  releaseDate,
  rawgUrl,
  rawgPlatforms,
  tags,
  notesPreview,
  favorite = false,
  showSelect = false,
  isSelected = false,
  onResolveRawgUrl,
  onImport,
  onRemove,
  onToggleSelect,
  onToggleFavorite,
  onOpenDetails,
  onUpdate,
  layout = "list",
}: GameCardProps) {
  const displayRating =
    rating === null || rating === undefined ? "N/A" : rating.toFixed(1)
  const displayPersonalRating =
    personalRating === null || personalRating === undefined
      ? ""
      : personalRating.toString()
  const showRemove = Boolean(onRemove)
  const showImport = Boolean(onImport) && !showRemove
  const isEditable = Boolean(onUpdate) && showRemove
  const [ratingInput, setRatingInput] = useState(displayPersonalRating)
  const [platformInput, setPlatformInput] = useState(platform ?? "")
  const [isUpdating, setIsUpdating] = useState(false)
  const isGrid = layout === "grid"
  const handleOpen = async () => {
    const url = rawgUrl ?? (onResolveRawgUrl ? await onResolveRawgUrl() : null)
    if (!url) {
      return
    }
    window.open(url, "_blank", "noopener,noreferrer")
  }
  const isClickable = Boolean(rawgUrl || onResolveRawgUrl)

  useEffect(() => {
    setRatingInput(displayPersonalRating)
  }, [displayPersonalRating])

  useEffect(() => {
    setPlatformInput(platform ?? "")
  }, [platform])

  const platformLabelMap: Record<string, string> = {
    PC: "PC",
    MAC: "Mac",
    LINUX: "Linux",
    PS1: "PS1",
    PS2: "PS2",
    PS3: "PS3",
    PS4: "PS4",
    PS5: "PS5",
    PS_VITA: "PS Vita",
    SWITCH: "Switch",
    SWITCH2: "Switch 2",
    DS: "DS",
    THREE_DS: "3DS",
    WII: "Wii",
    WII_U: "Wii U",
    GAMECUBE: "GameCube",
    N64: "Nintendo 64",
    SNES: "SNES",
    NES: "NES",
    GAMEBOY: "Game Boy",
    GAMEBOY_COLOR: "Game Boy Color",
    GAMEBOY_ADVANCE: "Game Boy Advance",
    PSP: "PSP",
    XBOX: "Xbox",
    XBOX_360: "Xbox 360",
    XBOX_ONE: "Xbox One",
    XBOX_SERIES: "Xbox Series",
  }

  const platformOptions = useMemo(() => {
    const normalized = (rawgPlatforms ?? []).map((name) => name.trim()).filter(Boolean)

    const mapRawgToEnum = (name: string): string | null => {
      const lower = name.toLowerCase()
      if (lower.includes("switch 2") || lower.includes("nintendo switch 2") || lower.includes("switch2")) {
        return "SWITCH2"
      }
      if (lower.includes("switch")) return "SWITCH"
      if (lower.includes("playstation 5") || lower.includes("ps5") || lower.includes("playstation5")) {
        return "PS5"
      }
      if (lower.includes("playstation 4") || lower.includes("ps4") || lower.includes("playstation4")) {
        return "PS4"
      }
      if (lower.includes("playstation 3") || lower.includes("ps3") || lower.includes("playstation3")) {
        return "PS3"
      }
      if (lower.includes("playstation 2") || lower.includes("ps2") || lower.includes("playstation2")) {
        return "PS2"
      }
      if (lower.includes("playstation portable") || lower.includes("psp")) {
        return "PSP"
      }
      if (lower.includes("playstation vita") || lower.includes("ps vita") || lower.includes("vita")) {
        return "PS_VITA"
      }
      if (lower.includes("3ds") || lower.includes("nintendo 3ds")) {
        return "THREE_DS"
      }
      if (lower.includes("nintendo ds") || (lower === "ds" && !lower.includes("3ds"))) {
        return "DS"
      }
      if (lower.includes("wii u")) return "WII_U"
      if (lower.includes("wii")) return "WII"
      if (lower.includes("gamecube")) return "GAMECUBE"
      if (lower.includes("nintendo 64") || lower.includes("n64")) return "N64"
      if (lower.includes("super nintendo") || lower.includes("snes")) return "SNES"
      if (lower.includes("nintendo entertainment system") || lower.includes("nes")) return "NES"
      if (lower.includes("game boy advance") || lower.includes("gba")) return "GAMEBOY_ADVANCE"
      if (lower.includes("game boy color") || lower.includes("gbc")) return "GAMEBOY_COLOR"
      if (lower.includes("game boy") || lower === "gb") return "GAMEBOY"
      if (lower.includes("xbox series") || lower.includes("series x") || lower.includes("series s")) {
        return "XBOX_SERIES"
      }
      if (lower.includes("xbox one")) return "XBOX_ONE"
      if (lower.includes("xbox 360")) return "XBOX_360"
      if (lower.includes("xbox")) return "XBOX"
      if (lower.includes("macos") || lower.includes("mac os") || lower === "mac") return "MAC"
      if (lower.includes("linux")) return "LINUX"
      if (lower.includes("pc") || lower.includes("windows")) return "PC"
      if (lower.includes("playstation") || lower.includes("ps1") || lower.includes("playstation1")) {
        return "PS1"
      }
      return null
    }

    const mapped = normalized
      .map((name) => ({
        label: name,
        value: mapRawgToEnum(name),
      }))
      .filter((option) => option.value)

    const deduped = new Map<string, string>()
    mapped.forEach((option) => {
      if (option.value && !deduped.has(option.value)) {
        deduped.set(option.value, option.label)
      }
    })

    const baseOptions =
      deduped.size > 0
        ? Array.from(deduped.entries()).map(([value, label]) => ({
            value,
            label,
          }))
        : [
            { value: "PC", label: "PC" },
            { value: "MAC", label: "Mac" },
            { value: "LINUX", label: "Linux" },
            { value: "PS1", label: "PS1" },
            { value: "PS2", label: "PS2" },
            { value: "PS3", label: "PS3" },
            { value: "PS4", label: "PS4" },
            { value: "PS5", label: "PS5" },
            { value: "PS_VITA", label: "PS Vita" },
            { value: "SWITCH", label: "Switch" },
            { value: "SWITCH2", label: "Switch 2" },
            { value: "DS", label: "DS" },
            { value: "THREE_DS", label: "3DS" },
            { value: "WII", label: "Wii" },
            { value: "WII_U", label: "Wii U" },
            { value: "GAMECUBE", label: "GameCube" },
            { value: "N64", label: "Nintendo 64" },
            { value: "SNES", label: "SNES" },
            { value: "NES", label: "NES" },
            { value: "GAMEBOY", label: "Game Boy" },
            { value: "GAMEBOY_COLOR", label: "Game Boy Color" },
            { value: "GAMEBOY_ADVANCE", label: "Game Boy Advance" },
            { value: "PSP", label: "PSP" },
            { value: "XBOX", label: "Xbox" },
            { value: "XBOX_360", label: "Xbox 360" },
            { value: "XBOX_ONE", label: "Xbox One" },
            { value: "XBOX_SERIES", label: "Xbox Series" },
          ]

    if (platform && !baseOptions.some((option) => option.value === platform)) {
      return [
        {
          value: platform,
          label: `${platformLabelMap[platform] ?? platform} (Current, not in RAWG)`,
        },
        ...baseOptions,
      ]
    }

    return baseOptions
  }, [rawgPlatforms, platform, platformLabelMap])

  const displayPlatform = platform
    ? platformLabelMap[platform] ?? platform
    : null

  const formattedPlayState = playState
    ? playState
        .toLowerCase()
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase())
    : "N/A"

  return (
    <div
      className={`flex w-full items-center gap-4 rounded-2xl border border-zinc-200 bg-gradient-to-br from-white via-zinc-50 to-zinc-100 p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-zinc-800 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900 ${isClickable ? "cursor-pointer" : ""} ${isGrid ? "flex-col items-start" : ""}`}
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
      <div className={`flex ${isGrid ? "w-full items-start gap-4" : "items-center gap-3"}`}>
        {showSelect && (
          <input
            type="checkbox"
            checked={isSelected}
            onChange={(event) => onToggleSelect?.(id, event.target.checked)}
            onClick={(event) => event.stopPropagation()}
            aria-label={`Select ${title}`}
            className="mt-1 h-4 w-4 rounded border-zinc-300 text-zinc-900"
          />
        )}
        <div className="relative h-20 w-14 flex-shrink-0 overflow-hidden rounded-lg bg-gradient-to-br from-zinc-200 to-zinc-100 dark:from-zinc-800 dark:to-zinc-700 sm:h-24 sm:w-16">
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
      </div>

      <div className={`flex w-full flex-col items-start gap-3 ${isGrid ? "" : "sm:flex-row sm:items-center sm:justify-between"}`}>
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
              Community {displayRating}
            </span>
            {personalRating !== null && personalRating !== undefined && (
              <span className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700">
                Personal {personalRating.toFixed(1)}
              </span>
            )}
            <span className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700">
              Play State {formattedPlayState}
            </span>
            {displayPlatform && (
              <span className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700">
                Platform {displayPlatform}
              </span>
            )}
            {releaseDate && (
              <span className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700">
                Released {releaseDate}
              </span>
            )}
          </div>
          {tags && tags.length > 0 && (
            <div className="flex flex-wrap gap-2 text-[11px] text-zinc-500 dark:text-zinc-400">
              {tags.map((tag) => (
                <span
                  key={`${id}-${tag}`}
                  className="rounded-full border border-zinc-200 px-2 py-0.5 dark:border-zinc-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
          {notesPreview && (
            <p className="max-w-md text-xs text-zinc-500 dark:text-zinc-400">
              Notes: {notesPreview}
            </p>
          )}
          {rawgPlatforms && rawgPlatforms.length > 0 && (
            <div className="flex flex-wrap gap-2 text-[11px] text-zinc-500 dark:text-zinc-400">
              <span className="font-semibold uppercase tracking-wide">Available</span>
              <span>{rawgPlatforms.join(", ")}</span>
            </div>
          )}
          {isEditable && (
            <div
              className="flex flex-wrap items-center gap-3 text-xs text-zinc-600 dark:text-zinc-300"
              onClick={(event) => event.stopPropagation()}
            >
              <label className="flex flex-col gap-1">
                Personal Rating
                <input
                  type="number"
                  min={0}
                  max={10}
                  step={0.1}
                  value={ratingInput}
                  onChange={(event) => setRatingInput(event.target.value)}
                  className="w-24 rounded-md border border-zinc-200 px-2 py-1 text-xs dark:border-zinc-700 dark:bg-zinc-900"
                />
              </label>
              <label className="flex flex-col gap-1">
                Platform
                <select
                  value={platformInput}
                  onChange={(event) => setPlatformInput(event.target.value)}
                  className="min-w-[140px] rounded-md border border-zinc-200 bg-white px-2 py-1 text-xs dark:border-zinc-700 dark:bg-zinc-900"
                >
                  {platformOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
              <button
                type="button"
                onClick={async (event) => {
                  event.stopPropagation()
                  if (!onUpdate) return
                  const nextRating = ratingInput.trim()
                  const parsedRating = nextRating === "" ? null : Number(nextRating)
                  if (nextRating !== "" && Number.isNaN(parsedRating)) {
                    return
                  }
                  setIsUpdating(true)
                  try {
                    await onUpdate(id, {
                      personal_rating: parsedRating,
                      platform: platformInput || null,
                    })
                  } finally {
                    setIsUpdating(false)
                  }
                }}
                disabled={isUpdating}
                className="mt-4 rounded-full bg-zinc-900 px-3 py-1.5 text-[11px] font-semibold text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-60 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-white"
              >
                {isUpdating ? "Saving..." : "Save"}
              </button>
            </div>
          )}
        </div>

        <div className={`flex w-full flex-wrap gap-2 ${isGrid ? "" : "sm:w-auto sm:justify-end"}`}>
          {onToggleFavorite && (
            <button
              onClick={(event) => {
                event.stopPropagation()
                onToggleFavorite(id, !favorite)
              }}
              className="rounded-full border border-zinc-300 px-3 py-2 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
            >
              {favorite ? "Unfavorite" : "Favorite"}
            </button>
          )}
          {onOpenDetails && (
            <button
              onClick={(event) => {
                event.stopPropagation()
                onOpenDetails(id)
              }}
              className="rounded-full border border-zinc-300 px-3 py-2 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
            >
              Details
            </button>
          )}
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
    </div>
  )
}
