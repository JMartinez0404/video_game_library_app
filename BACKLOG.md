# Video Game Library App Backlog

Last updated: 2026-03-14

Guidelines:
- Add new work items at the top of the Backlog list.
- When an item is completed, strike it out with Markdown (example: ~~Completed item~~).
- Keep items short and action-oriented.

Backlog:
- ~~Swap "Add to Library" for "Remove from Library" when viewing library entries.~~
- ~~Resolve duplicate POST `/external/video_games/{game_id}/import` route and remove dead `import_game` call.~~
- ~~Fix layering by moving `ExternalGameDTO` out of infrastructure and updating imports.~~
- ~~Add RAWG-to-Platform enum mapping in `ExternalGameService`.~~
- ~~Add API error handling for RAWG failures and expose clear response errors.~~
- ~~Create frontend API helpers in `frontend/lib/api/` and route all fetches through them.~~
- ~~Add loading and error states to the frontend search flow.~~
- ~~Display cover images and improve `GameCard` layout.~~
- ~~Add library filters and sorting in the backend and frontend.~~
- Add pagination for RAWG search results.
- Add rate limiting for external API calls.
- Add authentication for user libraries.
- Add tests for `ExternalGameService` with a fake RAWG client.
- Expand API route tests for external game endpoints.
- Add mobile-responsive layout improvements.

Done:
