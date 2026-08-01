export type VideoGame = {
  id: number
  title: string
  communal_rating?: number | null
  personal_rating?: number | null
  play_state?: string | null
  platform?: string | null
  image_url?: string | null
  release_date?: string | null
  rawg_slug?: string | null
  rawg_platforms?: string[] | null
  notes?: string | null
  tags?: string[] | null
  progress?: number | null
  favorite?: boolean | null
  added_at?: string | null
  last_updated?: string | null
}
