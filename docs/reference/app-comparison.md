# Field Maps vs Survey123

Both apps write to the same `HydrantInspections` table. This is how the two forms differ, which is what the [staff pilot](../setup/08-pilot.md) measures.

| | Survey123 | Field Maps |
|---|---|---|
| Account needed | Yes | Yes |
| Inspector list | Filtered by engine company | One searchable list |
| Issue checklist | One tap-list per section, saved as separate fields | One switch per issue |
| Needs Follow-up | Auto-set, crew can override | Auto-set, read-only |
| Hydrant details | Prefilled by the pop-up link | Filled from the related hydrant |
| Offline | Survey123 field app, but the hydrant must be opened from the link or picked manually | Full offline map with hydrants and their inspections |
| Photos | 2 photo questions; one required when follow-up is needed | Unlimited attachments, not forced |

## Things the pilot should show

- **Accounts.** Both apps need a sign-in, since the portal doesn't allow anonymous access.
- **Two apps or one.** Survey123 crews open the hydrant in Field Maps and jump to the survey, so they use both apps. Field Maps crews stay in one.
- **Fixing mistakes.** Field Maps crews can fix their own records afterwards; Survey123 crews can't once a record is sent.
