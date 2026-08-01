'use client'

import {
  getLibrary,
  importGame,
  backfillRawgSlugs,
  removeGame,
  searchExternalGames,
  updateGame,
  getActivity,
  getImportHistory,
  type ActivityItem,
  type ImportHistoryItem,
} from "@/lib/api/games"
import { useState, useEffect, useMemo } from "react"
import { VideoGame } from "@/types/videoGame"
import Image from "next/image"
import GameCard from "./GameCard"
import SearchBar from "@/components/SearchBar"

const PLATFORM_OPTIONS = [
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

function formatTimestamp(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

function parseYear(dateValue?: string | null) {
  if (!dateValue) return null
  const year = Number(dateValue.slice(0, 4))
  return Number.isNaN(year) ? null : year
}

export default function Home() {
  const project = "Digital Video Game Library"
  const searchPageSize = 10

  const [libraryGames, setLibraryGames] = useState<VideoGame[]>([])
  const [searchResults, setSearchResults] = useState<VideoGame[]>([])
  const [view, setView] = useState<"library" | "search">("library")
  const [isLoadingLibrary, setIsLoadingLibrary] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const [isLoadingMore, setIsLoadingMore] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)
  const [libraryError, setLibraryError] = useState<string | null>(null)
  const [isBackfilling, setIsBackfilling] = useState(false)
  const [backfillMessage, setBackfillMessage] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [searchPage, setSearchPage] = useState(1)
  const [searchTotal, setSearchTotal] = useState(0)
  const [filters, setFilters] = useState({
    play_state: "",
    sort_by: "title",
    sort_order: "asc" as "asc" | "desc",
  })
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([])
  const [librarySearch, setLibrarySearch] = useState("")
  const [ratingMin, setRatingMin] = useState("")
  const [ratingMax, setRatingMax] = useState("")
  const [yearMin, setYearMin] = useState("")
  const [yearMax, setYearMax] = useState("")
  const [tagFilter, setTagFilter] = useState("")
  const [favoritesOnly, setFavoritesOnly] = useState(false)
  const [sortPreset, setSortPreset] = useState("custom")
  const [viewMode, setViewMode] = useState<"list" | "grid">("list")
  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [bulkPlatform, setBulkPlatform] = useState("")
  const [bulkRating, setBulkRating] = useState("")

  const [activityLog, setActivityLog] = useState<ActivityItem[]>([])
  const [importHistory, setImportHistory] = useState<ImportHistoryItem[]>([])
  const [detailGameId, setDetailGameId] = useState<number | null>(null)
  const [detailNotes, setDetailNotes] = useState("")
  const [detailTags, setDetailTags] = useState("")
  const [detailProgress, setDetailProgress] = useState(0)
  const [hasAutoBackfilled, setHasAutoBackfilled] = useState(false)

  useEffect(() => {
    loadLibrary()
  }, [])

  async function refreshActivity() {
    const [activity, imports] = await Promise.all([
      getActivity(12),
      getImportHistory(10),
    ])
    setActivityLog(activity)
    setImportHistory(imports)
  }

  async function loadLibrary() {
    setIsLoadingLibrary(true)
    setLibraryError(null)
    setBackfillMessage(null)
    try {
      const data = await getLibrary()
      setLibraryGames(data)
      setView("library")
      setSelectedIds((prev) => prev.filter((id) => data.some((game) => game.id === id)))
      await refreshActivity()
    } catch (error) {
      setLibraryError(
        error instanceof Error ? error.message : "Failed to load library.",
      )
    } finally {
      setIsLoadingLibrary(false)
    }
  }

  async function handleSearch(query: string) {
    const trimmed = query.trim()
    if (!trimmed) {
      setSearchError("Enter a game name to search.")
      return
    }

    setIsSearching(true)
    setSearchError(null)
    try {
      const response = await searchExternalGames(trimmed, 1, searchPageSize)
      setSearchResults(response.results)
      setSearchQuery(trimmed)
      setSearchPage(1)
      setSearchTotal(response.count)
      setView("search")
    } catch (error) {
      setSearchError(
        error instanceof Error ? error.message : "Search failed. Try again.",
      )
    } finally {
      setIsSearching(false)
    }
  }

  async function handleImport(id: number) {
    try {
      await importGame(id)
      await loadLibrary()
    } catch (error) {
      setLibraryError(
        error instanceof Error ? error.message : "Import failed.",
      )
    }
  }

  async function handleRemove(title: string) {
    await removeGame(title)
    await loadLibrary()
  }

  async function applyUpdate(id: number, update: Parameters<typeof updateGame>[1]) {
    const updated = await updateGame(id, update)
    setLibraryGames((prev) =>
      prev.map((game) => (game.id === id ? updated : game)),
    )
    await refreshActivity()
    return updated
  }

  async function handleUpdate(
    id: number,
    update: { personal_rating?: number | null; platform?: string | null },
  ) {
    try {
      await applyUpdate(id, update)
    } catch (error) {
      setLibraryError(
        error instanceof Error ? error.message : "Update failed.",
      )
    }
  }

  async function handleBulkUpdate() {
    if (selectedIds.length === 0) return
    const nextPlatform = bulkPlatform || null
    const ratingValue = bulkRating.trim()
    const nextRating = ratingValue === "" ? null : Number(ratingValue)
    if (ratingValue !== "" && Number.isNaN(nextRating)) {
      setLibraryError("Enter a valid rating or leave it blank.")
      return
    }
    if (!nextPlatform && nextRating === null) {
      setLibraryError("Select a platform or rating to apply.")
      return
    }

    setLibraryError(null)
    try {
      await Promise.all(
        selectedIds.map((gameId) =>
          updateGame(gameId, {
            personal_rating: nextRating === null ? undefined : nextRating,
            platform: nextPlatform ?? undefined,
          }),
        ),
      )
      setSelectedIds([])
      setBulkPlatform("")
      setBulkRating("")
      await loadLibrary()
    } catch (error) {
      setLibraryError(
        error instanceof Error ? error.message : "Bulk update failed.",
      )
    }
  }

  async function handleUndoImport(entry: ImportHistoryItem) {
    const game = libraryGames.find((item) => item.id === entry.game_id)
    if (!game) return
    await handleRemove(game.title)
  }

  function handleToggleSelect(id: number, selected: boolean) {
    setSelectedIds((prev) => {
      if (selected) {
        return prev.includes(id) ? prev : [...prev, id]
      }
      return prev.filter((item) => item !== id)
    })
  }

  async function handleToggleFavorite(id: number, next: boolean) {
    try {
      await applyUpdate(id, { favorite: next })
    } catch (error) {
      setLibraryError(
        error instanceof Error ? error.message : "Favorite update failed.",
      )
    }
  }

  function handleOpenDetails(id: number) {
    setDetailGameId(id)
  }

  function closeDetails() {
    setDetailGameId(null)
  }

  function buildRawgUrl(game: VideoGame): string | null {
    if (game.rawg_slug) {
      return `https://rawg.io/games/${game.rawg_slug}`
    }
    return null
  }

  function slugifyTitle(title: string): string {
    return title
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)+/g, "")
  }

  function normalizeTitle(title: string): string {
    return title
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "")
  }

  async function resolveRawgUrl(game: VideoGame): Promise<string | null> {
    if (game.rawg_slug) {
      return `https://rawg.io/games/${game.rawg_slug}`
    }
    if (!game.title) {
      return null
    }

    try {
      const response = await searchExternalGames(game.title, 1, 20)
      const releaseDate = game.release_date?.slice(0, 10)
      if (releaseDate) {
        const matchByDate = response.results.find(
          (result) => result.release_date?.slice(0, 10) === releaseDate,
        )
        if (matchByDate?.rawg_slug) {
          return `https://rawg.io/games/${matchByDate.rawg_slug}`
        }
      }

      const normalizedTitle = normalizeTitle(game.title)
      const matchByTitle = response.results.find(
        (result) =>
          result.title && normalizeTitle(result.title) === normalizedTitle,
      )
      if (matchByTitle?.rawg_slug) {
        return `https://rawg.io/games/${matchByTitle.rawg_slug}`
      }
    } catch (error) {
      setSearchError(
        error instanceof Error ? error.message : "Search failed. Try again.",
      )
    }

    const slug = slugifyTitle(game.title)
    return slug ? `https://rawg.io/games/${slug}` : null
  }

  async function handleBackfill(mode: "manual" | "auto" = "manual") {
    setIsBackfilling(true)
    if (mode === "manual") {
      setBackfillMessage(null)
    }
    try {
      const result = await backfillRawgSlugs()
      await loadLibrary()
      const label = mode === "auto" ? "Auto backfill" : "Backfill"
      setBackfillMessage(
        `${label} complete: ${result.updated} updated, ${result.skipped} skipped, ${result.failed} failed.`,
      )
    } catch (error) {
      setBackfillMessage(
        error instanceof Error
          ? error.message
          : "Backfill failed. Try again.",
      )
    } finally {
      setIsBackfilling(false)
    }
  }

  async function handleLoadMore() {
    if (!searchQuery || isLoadingMore) {
      return
    }
    const nextPage = searchPage + 1
    setIsLoadingMore(true)
    setSearchError(null)
    try {
      const response = await searchExternalGames(
        searchQuery,
        nextPage,
        searchPageSize,
      )
      setSearchResults((prev) => [...prev, ...response.results])
      setSearchPage(nextPage)
      setSearchTotal(response.count)
    } catch (error) {
      setSearchError(
        error instanceof Error ? error.message : "Search failed. Try again.",
      )
    } finally {
      setIsLoadingMore(false)
    }
  }

  useEffect(() => {
    if (
      view !== "library" ||
      isBackfilling ||
      hasAutoBackfilled ||
      libraryGames.length === 0
    ) {
      return
    }
    const needsBackfill = libraryGames.some(
      (game) =>
        !game.rawg_slug ||
        !game.rawg_platforms ||
        game.rawg_platforms.length === 0,
    )
    if (!needsBackfill) {
      return
    }
    setHasAutoBackfilled(true)
    void handleBackfill("auto")
  }, [view, libraryGames, isBackfilling, hasAutoBackfilled])

  const filteredLibraryGames = useMemo(() => {
    let result = [...libraryGames]

    if (librarySearch.trim()) {
      const term = librarySearch.trim().toLowerCase()
      result = result.filter((game) => game.title.toLowerCase().includes(term))
    }

    if (filters.play_state) {
      result = result.filter((game) => game.play_state === filters.play_state)
    }

    if (selectedPlatforms.length > 0) {
      result = result.filter(
        (game) => game.platform && selectedPlatforms.includes(game.platform),
      )
    }

    if (ratingMin.trim()) {
      const min = Number(ratingMin)
      if (!Number.isNaN(min)) {
        result = result.filter(
          (game) => (game.communal_rating ?? 0) >= min,
        )
      }
    }

    if (ratingMax.trim()) {
      const max = Number(ratingMax)
      if (!Number.isNaN(max)) {
        result = result.filter(
          (game) => (game.communal_rating ?? 0) <= max,
        )
      }
    }

    if (yearMin.trim()) {
      const min = Number(yearMin)
      if (!Number.isNaN(min)) {
        result = result.filter((game) => {
          const year = parseYear(game.release_date)
          return year !== null && year >= min
        })
      }
    }

    if (yearMax.trim()) {
      const max = Number(yearMax)
      if (!Number.isNaN(max)) {
        result = result.filter((game) => {
          const year = parseYear(game.release_date)
          return year !== null && year <= max
        })
      }
    }

    if (favoritesOnly) {
      result = result.filter((game) => game.favorite)
    }

    if (tagFilter.trim()) {
      const needle = tagFilter.trim().toLowerCase()
      result = result.filter((game) => {
        const tags = game.tags ?? []
        return tags.some((tag) => tag.toLowerCase().includes(needle))
      })
    }

    if (sortPreset === "recent") {
      result.sort((a, b) => (b.added_at ?? "").localeCompare(a.added_at ?? ""))
    } else if (sortPreset === "highest") {
      result.sort((a, b) => (b.communal_rating ?? 0) - (a.communal_rating ?? 0))
    } else if (sortPreset === "personal") {
      result.sort(
        (a, b) => (b.personal_rating ?? 0) - (a.personal_rating ?? 0),
      )
    } else {
      result.sort((a, b) => {
        const field = filters.sort_by as keyof VideoGame
        const aValue = a[field] ?? ""
        const bValue = b[field] ?? ""
        if (aValue < bValue) return filters.sort_order === "asc" ? -1 : 1
        if (aValue > bValue) return filters.sort_order === "asc" ? 1 : -1
        return 0
      })
    }

    return result
  }, [
    libraryGames,
    librarySearch,
    filters.play_state,
    filters.sort_by,
    filters.sort_order,
    selectedPlatforms,
    ratingMin,
    ratingMax,
    yearMin,
    yearMax,
    favoritesOnly,
    tagFilter,
    sortPreset,
  ])

  const stats = useMemo(() => {
    const total = filteredLibraryGames.length
    const byPlatform: Record<string, number> = {}
    const byState: Record<string, number> = {}
    const ratingBuckets: Record<string, number> = {
      "0-2": 0,
      "2-4": 0,
      "4-6": 0,
      "6-8": 0,
      "8-10": 0,
    }

    filteredLibraryGames.forEach((game) => {
      const platform = game.platform ?? "Unknown"
      byPlatform[platform] = (byPlatform[platform] ?? 0) + 1

      const state = game.play_state ?? "Unknown"
      byState[state] = (byState[state] ?? 0) + 1

      if (game.communal_rating !== null && game.communal_rating !== undefined) {
        const rating = game.communal_rating
        if (rating < 2) ratingBuckets["0-2"] += 1
        else if (rating < 4) ratingBuckets["2-4"] += 1
        else if (rating < 6) ratingBuckets["4-6"] += 1
        else if (rating < 8) ratingBuckets["6-8"] += 1
        else ratingBuckets["8-10"] += 1
      }
    })

    return { total, byPlatform, byState, ratingBuckets }
  }, [filteredLibraryGames])

  const detailGame = useMemo(
    () => libraryGames.find((game) => game.id === detailGameId) ?? null,
    [detailGameId, libraryGames],
  )

  useEffect(() => {
    if (!detailGame) {
      setDetailNotes("")
      setDetailTags("")
      setDetailProgress(0)
      return
    }
    setDetailNotes(detailGame.notes ?? "")
    setDetailTags((detailGame.tags ?? []).join(", "))
    setDetailProgress(detailGame.progress ?? 0)
  }, [detailGame])

  useEffect(() => {
    if (!detailGame) return
    const handler = setTimeout(async () => {
      if (detailNotes !== (detailGame.notes ?? "")) {
        await applyUpdate(detailGame.id, { notes: detailNotes })
      }
    }, 600)
    return () => clearTimeout(handler)
  }, [detailNotes, detailGame])

  useEffect(() => {
    if (!detailGame) return
    const handler = setTimeout(async () => {
      const tags = detailTags
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean)
      const current = detailGame.tags ?? []
      if (tags.join("|") !== current.join("|")) {
        await applyUpdate(detailGame.id, { tags })
      }
    }, 600)
    return () => clearTimeout(handler)
  }, [detailTags, detailGame])

  useEffect(() => {
    if (!detailGame) return
    const handler = setTimeout(async () => {
      const current = detailGame.progress ?? 0
      if (detailProgress !== current) {
        await applyUpdate(detailGame.id, { progress: detailProgress })
      }
    }, 400)
    return () => clearTimeout(handler)
  }, [detailProgress, detailGame])

  function updateFilters(patch: Partial<typeof filters>) {
    setFilters((prev) => ({ ...prev, ...patch }))
    setView("library")
  }

  function togglePlatformFilter(value: string) {
    setSelectedPlatforms((prev) =>
      prev.includes(value) ? prev.filter((item) => item !== value) : [...prev, value],
    )
  }

  function handleRandomPick() {
    if (filteredLibraryGames.length === 0) return
    const pick =
      filteredLibraryGames[Math.floor(Math.random() * filteredLibraryGames.length)]
    setDetailGameId(pick.id)
  }

  const displayedGames = view === "library" ? filteredLibraryGames : searchResults

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-6xl flex-col items-center justify-between bg-white px-6 py-16 dark:bg-black sm:items-start sm:px-10 sm:py-24 lg:px-16 lg:py-32">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />
        <div className="flex w-full flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50 sm:max-w-md">
            {project}
          </h1>

          <SearchBar onSearch={handleSearch} isLoading={isSearching} />
          {searchError && (
            <p className="text-sm text-red-600" role="alert">
              {searchError}
            </p>
          )}

          {view === "library" ? (
            <div className="flex w-full flex-col gap-4 rounded-2xl border border-zinc-200 bg-white p-4 text-sm text-zinc-700 shadow-sm dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-200">
              <div className="flex flex-wrap items-center gap-3">
                <label className="flex flex-col gap-1">
                  Search Library
                  <input
                    value={librarySearch}
                    onChange={(event) => setLibrarySearch(event.target.value)}
                    placeholder="Search by title"
                    className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>

                <label className="flex flex-col gap-1">
                  Play State
                  <select
                    value={filters.play_state}
                    onChange={(e) => updateFilters({ play_state: e.target.value })}
                    className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  >
                    <option value="">All</option>
                    <option value="NOT_STARTED">Not started</option>
                    <option value="STARTED">Started</option>
                    <option value="PLAYED_ENOUGH">Played enough</option>
                    <option value="BEATEN">Beaten</option>
                    <option value="PLAY_AGAIN">Play again</option>
                  </select>
                </label>

                <label className="flex flex-col gap-1">
                  Sort Preset
                  <select
                    value={sortPreset}
                    onChange={(event) => setSortPreset(event.target.value)}
                    className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  >
                    <option value="custom">Custom</option>
                    <option value="recent">Recently Added</option>
                    <option value="highest">Highest Community Rating</option>
                    <option value="personal">Highest Personal Rating</option>
                  </select>
                </label>

                {sortPreset === "custom" && (
                  <>
                    <label className="flex flex-col gap-1">
                      Sort By
                      <select
                        value={filters.sort_by}
                        onChange={(e) => updateFilters({ sort_by: e.target.value })}
                        className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                      >
                        <option value="title">Title</option>
                        <option value="communal_rating">Community Rating</option>
                        <option value="personal_rating">Personal Rating</option>
                        <option value="release_date">Release Date</option>
                      </select>
                    </label>

                    <label className="flex flex-col gap-1">
                      Order
                      <select
                        value={filters.sort_order}
                        onChange={(e) =>
                          updateFilters({
                            sort_order: (e.target.value as "asc" | "desc") || "asc",
                          })
                        }
                        className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                      >
                        <option value="asc">Ascending</option>
                        <option value="desc">Descending</option>
                      </select>
                    </label>
                  </>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <label className="flex flex-col gap-1">
                  Rating Min
                  <input
                    value={ratingMin}
                    onChange={(event) => setRatingMin(event.target.value)}
                    placeholder="0"
                    className="w-20 rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <label className="flex flex-col gap-1">
                  Rating Max
                  <input
                    value={ratingMax}
                    onChange={(event) => setRatingMax(event.target.value)}
                    placeholder="10"
                    className="w-20 rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <label className="flex flex-col gap-1">
                  Year Min
                  <input
                    value={yearMin}
                    onChange={(event) => setYearMin(event.target.value)}
                    placeholder="1980"
                    className="w-24 rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <label className="flex flex-col gap-1">
                  Year Max
                  <input
                    value={yearMax}
                    onChange={(event) => setYearMax(event.target.value)}
                    placeholder="2024"
                    className="w-24 rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <label className="flex flex-col gap-1">
                  Tag Filter
                  <input
                    value={tagFilter}
                    onChange={(event) => setTagFilter(event.target.value)}
                    placeholder="metroidvania"
                    className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={favoritesOnly}
                    onChange={(event) => setFavoritesOnly(event.target.checked)}
                  />
                  Favorites only
                </label>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <span className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Platforms
                </span>
                {PLATFORM_OPTIONS.map((option) => (
                  <label key={option.value} className="flex items-center gap-2 text-xs">
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(option.value)}
                      onChange={() => togglePlatformFilter(option.value)}
                    />
                    {option.label}
                  </label>
                ))}
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={handleRandomPick}
                  className="rounded-full border border-zinc-300 px-3 py-1.5 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 disabled:cursor-not-allowed disabled:opacity-60 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
                >
                  Random Pick
                </button>
                <button
                  type="button"
                  onClick={() => setViewMode(viewMode === "list" ? "grid" : "list")}
                  className="rounded-full border border-zinc-300 px-3 py-1.5 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
                >
                  {viewMode === "list" ? "Grid View" : "List View"}
                </button>
                <button
                  type="button"
                  onClick={() => handleBackfill("manual")}
                  disabled={isBackfilling}
                  className="rounded-full border border-zinc-300 px-3 py-1.5 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 disabled:cursor-not-allowed disabled:opacity-60 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
                >
                  {isBackfilling ? "Backfilling..." : "Backfill RAWG Links"}
                </button>
                {backfillMessage && (
                  <span className="text-xs text-zinc-500">{backfillMessage}</span>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-3 rounded-xl border border-dashed border-zinc-200 p-3 text-xs dark:border-zinc-700">
                <span className="font-semibold text-zinc-600 dark:text-zinc-300">
                  Bulk Edit
                </span>
                <span className="text-zinc-500">Selected: {selectedIds.length}</span>
                <select
                  value={bulkPlatform}
                  onChange={(event) => setBulkPlatform(event.target.value)}
                  className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-xs dark:border-zinc-700 dark:bg-zinc-900"
                >
                  <option value="">Platform (optional)</option>
                  {PLATFORM_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
                <input
                  value={bulkRating}
                  onChange={(event) => setBulkRating(event.target.value)}
                  placeholder="Personal rating"
                  className="w-28 rounded-md border border-zinc-200 bg-white px-2 py-1 text-xs dark:border-zinc-700 dark:bg-zinc-900"
                />
                <button
                  type="button"
                  onClick={handleBulkUpdate}
                  className="rounded-full bg-zinc-900 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-black dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-white"
                >
                  Apply to Selected
                </button>
              </div>

              {libraryError && (
                <p className="text-sm text-red-600" role="alert">
                  {libraryError}
                </p>
              )}
              {isLoadingLibrary && (
                <p className="text-sm text-zinc-500">Loading library...</p>
              )}

              <div className="grid gap-4 text-xs text-zinc-600 dark:text-zinc-300 md:grid-cols-3">
                <div className="rounded-xl border border-zinc-200 p-3 dark:border-zinc-800">
                  <p className="font-semibold text-zinc-700 dark:text-zinc-200">
                    Library Stats
                  </p>
                  <p>Total games: {stats.total}</p>
                  <p>
                    Favorites: {filteredLibraryGames.filter((game) => game.favorite).length}
                  </p>
                </div>
                <div className="rounded-xl border border-zinc-200 p-3 dark:border-zinc-800">
                  <p className="font-semibold text-zinc-700 dark:text-zinc-200">
                    By Platform
                  </p>
                  {Object.entries(stats.byPlatform).map(([platform, count]) => (
                    <p key={platform}>
                      {platform}: {count}
                    </p>
                  ))}
                </div>
                <div className="rounded-xl border border-zinc-200 p-3 dark:border-zinc-800">
                  <p className="font-semibold text-zinc-700 dark:text-zinc-200">
                    Rating Spread
                  </p>
                  {Object.entries(stats.ratingBuckets).map(([bucket, count]) => (
                    <p key={bucket}>
                      {bucket}: {count}
                    </p>
                  ))}
                </div>
              </div>

              <div className="grid gap-4 text-xs text-zinc-600 dark:text-zinc-300 md:grid-cols-2">
                <div className="rounded-xl border border-zinc-200 p-3 dark:border-zinc-800">
                  <p className="font-semibold text-zinc-700 dark:text-zinc-200">
                    Activity Feed
                  </p>
                  <div className="mt-2 h-40 overflow-y-auto pr-2">
                    {activityLog.length === 0 ? (
                      <p className="text-zinc-500">No recent activity yet.</p>
                    ) : (
                      activityLog.map((item) => (
                        <p key={item.id}>
                          {formatTimestamp(item.timestamp)} — {item.type} {item.title}
                          {item.details ? ` (${item.details})` : ""}
                        </p>
                      ))
                    )}
                  </div>
                </div>
                <div className="rounded-xl border border-zinc-200 p-3 dark:border-zinc-800">
                  <p className="font-semibold text-zinc-700 dark:text-zinc-200">
                    Import History
                  </p>
                  {importHistory.length === 0 ? (
                    <p className="text-zinc-500">No imports recorded.</p>
                  ) : (
                    importHistory.map((entry) => (
                      <div key={entry.game_id} className="flex items-center gap-2">
                        <span>
                          {entry.title} — {formatTimestamp(entry.timestamp)}
                        </span>
                        <button
                          type="button"
                          onClick={() => handleUndoImport(entry)}
                          className="rounded-full border border-zinc-300 px-2 py-1 text-[11px] font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
                        >
                          Undo
                        </button>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => loadLibrary()}
              className="text-sm font-semibold text-zinc-700 underline decoration-zinc-300 underline-offset-4 hover:text-zinc-900 dark:text-zinc-200 dark:decoration-zinc-600 dark:hover:text-white"
            >
              Back to Library
            </button>
          )}

          {view === "library" && libraryGames.length === 0 && !isLoadingLibrary && (
            <div className="w-full rounded-2xl border border-dashed border-zinc-200 p-6 text-sm text-zinc-600 dark:border-zinc-700 dark:text-zinc-300">
              <p className="font-semibold">Your library is empty.</p>
              <p>
                Try searching above to add games, then tag favorites, track progress,
                and build your backlog.
              </p>
            </div>
          )}

          <div
            className={
              viewMode === "grid"
                ? "grid w-full grid-cols-1 gap-4 md:grid-cols-2"
                : "flex w-full flex-col gap-4"
            }
          >
            {displayedGames.map((game) => (
              <GameCard
                key={game.id}
                id={game.id}
                title={game.title}
                rating={game.communal_rating}
                personalRating={game.personal_rating}
                playState={game.play_state}
                platform={game.platform}
                imageUrl={game.image_url}
                releaseDate={game.release_date}
                rawgUrl={buildRawgUrl(game)}
                rawgPlatforms={game.rawg_platforms}
                tags={game.tags ?? []}
                notesPreview={game.notes ? game.notes.slice(0, 120) : null}
                favorite={Boolean(game.favorite)}
                showSelect={view === "library"}
                isSelected={selectedIds.includes(game.id)}
                onToggleSelect={handleToggleSelect}
                onToggleFavorite={view === "library" ? handleToggleFavorite : undefined}
                onOpenDetails={view === "library" ? handleOpenDetails : undefined}
                onResolveRawgUrl={() => resolveRawgUrl(game)}
                onImport={view === "search" ? handleImport : undefined}
                onRemove={view === "library" ? handleRemove : undefined}
                onUpdate={view === "library" ? handleUpdate : undefined}
                layout={viewMode}
              />
            ))}
          </div>

          {view === "search" && searchResults.length < searchTotal && (
            <button
              type="button"
              onClick={handleLoadMore}
              disabled={isLoadingMore}
              className="rounded-full border border-zinc-300 px-4 py-2 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 disabled:cursor-not-allowed disabled:opacity-60 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
            >
              {isLoadingMore ? "Loading..." : "Load more"}
            </button>
          )}
        </div>

        {detailGame && (
          <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 p-6 sm:items-center">
            <div className="w-full max-w-2xl rounded-2xl bg-white p-6 text-left shadow-xl dark:bg-zinc-950">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-wide text-zinc-500">
                    Game Details
                  </p>
                  <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">
                    {detailGame.title}
                  </h2>
                </div>
                <button
                  type="button"
                  onClick={closeDetails}
                  className="rounded-full border border-zinc-300 px-3 py-1 text-xs font-semibold text-zinc-700 transition hover:border-zinc-400 hover:text-zinc-900 dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500 dark:hover:text-white"
                >
                  Close
                </button>
              </div>

              <div className="mt-4 grid gap-4 text-sm text-zinc-600 dark:text-zinc-300 md:grid-cols-[140px_1fr]">
                <div className="h-40 w-28 overflow-hidden rounded-xl bg-zinc-200 dark:bg-zinc-800">
                  {detailGame.image_url ? (
                    <img
                      src={detailGame.image_url}
                      alt={`${detailGame.title} cover`}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center text-xs text-zinc-500">
                      No Image
                    </div>
                  )}
                </div>
                <div className="space-y-2">
                  <p>Platform: {detailGame.platform ?? "Unknown"}</p>
                  <p>Play State: {detailGame.play_state ?? "Unknown"}</p>
                  <p>
                    Community Rating: {detailGame.communal_rating ?? "N/A"}
                  </p>
                  <p>Personal Rating: {detailGame.personal_rating ?? "N/A"}</p>
                  <p>Release Date: {detailGame.release_date ?? "Unknown"}</p>
                  <p>Added: {detailGame.added_at ? formatTimestamp(detailGame.added_at) : "Unknown"}</p>
                  <p>
                    Last Updated: {detailGame.last_updated ? formatTimestamp(detailGame.last_updated) : "Unknown"}
                  </p>
                </div>
              </div>

              <div className="mt-4 grid gap-4 text-sm text-zinc-600 dark:text-zinc-300 md:grid-cols-2">
                <label className="flex flex-col gap-1 text-xs">
                  Notes (autosave)
                  <textarea
                    value={detailNotes}
                    onChange={(event) => setDetailNotes(event.target.value)}
                    className="min-h-[80px] rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  />
                </label>
                <div className="space-y-3">
                  <label className="flex flex-col gap-1 text-xs">
                    Tags (comma separated)
                    <input
                      value={detailTags}
                      onChange={(event) => setDetailTags(event.target.value)}
                      className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                    />
                  </label>
                  <label className="flex flex-col gap-1 text-xs">
                    Progress: {detailProgress}%
                    <input
                      type="range"
                      min={0}
                      max={100}
                      step={1}
                      value={detailProgress}
                      onChange={(event) => setDetailProgress(Number(event.target.value))}
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
