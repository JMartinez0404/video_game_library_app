"use client"

import { useState } from "react"

type SearchBarProps = {
  onSearch: (query: string) => void | Promise<void>
  isLoading?: boolean
}

export default function SearchBar({ onSearch, isLoading = false }: SearchBarProps) {

  const [query, setQuery] = useState("")

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3">
      <input
        type="text"
        placeholder="Search games..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isLoading}
        className="w-72 rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-800 shadow-sm outline-none focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100 sm:w-96"
      />

      <button
        type="submit"
        disabled={isLoading}
        className="rounded-md bg-zinc-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-black disabled:cursor-not-allowed disabled:opacity-60 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-white"
      >
        {isLoading ? "Searching..." : "Search"}
      </button>
    </form>
  )
}
