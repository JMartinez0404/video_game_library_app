'use client'

import {
  getLibraryWithQuery,
  importGame,
  removeGame,
  searchExternalGames,
  type LibraryQuery,
} from "@/lib/api/games"
import { useState, useEffect } from "react"
import { VideoGame } from "@/types/videoGame"
import Image from "next/image";
import GameCard from "./GameCard"
import SearchBar from "@/components/SearchBar"


export default function Home() {
  const project = "Digital Video Game Library"
  const [games, setGames] = useState<VideoGame[]>([])
  const [view, setView] = useState<"library" | "search">("library")
  const [isLoadingLibrary, setIsLoadingLibrary] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const [searchError, setSearchError] = useState<string | null>(null)
  const [libraryError, setLibraryError] = useState<string | null>(null)
  const [filters, setFilters] = useState<LibraryQuery>({
    sort_by: "title",
    sort_order: "asc",
  })

  useEffect(() => {
    loadLibrary(filters)
  }, [])

  async function loadLibrary(nextFilters: LibraryQuery) {
    setIsLoadingLibrary(true)
    setLibraryError(null)
    try {
      const data = await getLibraryWithQuery(nextFilters)
      setGames(data)
      setView("library")
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
      const results = await searchExternalGames(trimmed)
      setGames(results)
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
    await importGame(id)

    await loadLibrary(filters)
  }

  async function handleRemove(title: string) {
    await removeGame(title)
    await loadLibrary(filters)
  }

  function updateFilters(patch: Partial<LibraryQuery>) {
    const nextFilters = { ...filters, ...patch }
    setFilters(nextFilters)
    loadLibrary(nextFilters)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={100}
          height={20}
          priority
        />
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            {project}
          </h1>

          <SearchBar onSearch={handleSearch} isLoading={isSearching} />
          {searchError && (
            <p className="text-sm text-red-600" role="alert">
              {searchError}
            </p>
          )}

          {view === "library" ? (
            <div className="flex w-full flex-col gap-3 rounded-2xl border border-zinc-200 bg-white p-4 text-sm text-zinc-700 shadow-sm dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-200">
              <div className="flex flex-wrap items-center gap-3">
                <label className="flex flex-col gap-1">
                  Platform
                  <select
                    value={filters.platform ?? ""}
                    onChange={(e) =>
                      updateFilters({ platform: e.target.value || undefined })
                    }
                    className="rounded-md border border-zinc-200 bg-white px-2 py-1 text-sm dark:border-zinc-700 dark:bg-zinc-900"
                  >
                    <option value="">All</option>
                    <option value="PS1">PS1</option>
                    <option value="PS2">PS2</option>
                    <option value="PS3">PS3</option>
                    <option value="PS4">PS4</option>
                    <option value="PS5">PS5</option>
                    <option value="SWITCH">Switch</option>
                    <option value="SWITCH2">Switch 2</option>
                    <option value="DS">DS</option>
                    <option value="THREE_DS">3DS</option>
                    <option value="WII">Wii</option>
                    <option value="PSP">PSP</option>
                    <option value="XBOX">Xbox</option>
                  </select>
                </label>

                <label className="flex flex-col gap-1">
                  Play State
                  <select
                    value={filters.play_state ?? ""}
                    onChange={(e) =>
                      updateFilters({ play_state: e.target.value || undefined })
                    }
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
                  Sort By
                  <select
                    value={filters.sort_by ?? "title"}
                    onChange={(e) =>
                      updateFilters({ sort_by: e.target.value || undefined })
                    }
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
                    value={filters.sort_order ?? "asc"}
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
              </div>
              {libraryError && (
                <p className="text-sm text-red-600" role="alert">
                  {libraryError}
                </p>
              )}
              {isLoadingLibrary && (
                <p className="text-sm text-zinc-500">Loading library...</p>
              )}
            </div>
          ) : (
            <button
              type="button"
              onClick={() => loadLibrary(filters)}
              className="text-sm font-semibold text-zinc-700 underline decoration-zinc-300 underline-offset-4 hover:text-zinc-900 dark:text-zinc-200 dark:decoration-zinc-600 dark:hover:text-white"
            >
              Back to Library
            </button>
          )}

          {games.map((game) => (
            <GameCard
              key={game.id}
              id={game.id}
              title={game.title}
              rating={game.communal_rating}
              imageUrl={game.image_url}
              releaseDate={game.release_date}
              onImport={view === "search" ? handleImport : undefined}
              onRemove={view === "library" ? handleRemove : undefined}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
