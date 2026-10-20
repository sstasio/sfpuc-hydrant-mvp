# Field Maps vs Survey123

Both apps write to the same `HydrantInspections` table. This is how the two forms differ, which is what the [staff pilot](../setup/08-pilot.md) measures.

| | Survey123 | Field Maps |
|---|---|---|
| Account needed | Optional (public survey) | Yes |
| Inspector list | Filtered by engine company | One searchable list |
| Issue checklist | One tap-list per section, saved as separate fields | One switch per issue |
| Needs Follow-up | Auto-set, crew can override | Auto-set, read-only |
| Hydrant details | Prefilled by the pop-up link | Filled from the related hydrant |
| Offline | Survey123 field app, but the hydrant must be opened from the link or picked manually | Full offline map with hydrants and their inspections |
| Photos | 2 photo questions; one required when follow-up is needed | Unlimited attachments, not forced |

## Things the pilot should show

- **Accounts.** Field Maps always needs a sign-in. Survey123 can skip it, but only if the portal allows public sharing.
- **No-account crews lose the map.** Without a sign-in they can't open the Field Maps map, so they open Survey123 directly and type the GIS ID. Those records arrive with no link to the hydrant (empty `HydrantGUID`). If Survey123 wins on accounts, a nightly FME or Python job that matches GIS ID to hydrant would close the gap.
- **Public-view records can't be fixed from the app.** They have no SFPUC user in `created_user`. The Inspector pick list still records who did the inspection, and the GIS team can correct records in the source.
