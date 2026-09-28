# User Roles & Permission Table

| Action | Student | Teacher | Admin |
|---|:---:|:---:|:---:|
| Register / Login | ✅ | ✅ | ✅ |
| View assignments | ✅ | ✅ | ✅ |
| Create / update / delete assignment | ❌ | ✅ (own only) | ✅ |
| Upload / resubmit assignment | ✅ | ❌ | ❌ |
| View own submissions | ✅ | — | — |
| View all submissions for an assignment | ❌ | ✅ (own courses) | ✅ |
| Download own submission | ✅ | — | — |
| Download any student's submission | ❌ | ✅ (own courses) | ✅ |
| Grade a submission | ❌ | ✅ | ✅ |
| View own marks/feedback | ✅ | — | — |
| View student dashboard | ✅ | ❌ | ❌ |
| View teacher dashboard | ❌ | ✅ | ✅ |
| Manage users / assign teacher roles | ❌ | ❌ | ✅ (future scope — not yet built) |

Enforced in code by `auth_utils.role_required()` plus explicit ownership
checks inside each route (see `docs/SECURITY.md`).
