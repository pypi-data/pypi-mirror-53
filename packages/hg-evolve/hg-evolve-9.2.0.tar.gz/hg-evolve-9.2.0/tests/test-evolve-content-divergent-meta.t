+====================================================
+Tests the resolution of content divergence: metadata
+====================================================

This file intend to cover cases focused around meta data merging.

Setup
-----

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n {phase} {instabilities}\n\n"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

Check we preserve the author properly
-------------------------------------

Testing issue6113 to make sure that content-divergence resolution don't
replace initial author with the user running the resolution command:

  $ hg init userfoo
  $ cd userfoo
  $ unset HGUSER
  $ echo "[ui]" >> ./.hg/hgrc
  $ echo "username = foo <foo@test.com>" >> ./.hg/hgrc
  $ for ch in a b c; do
  > echo $ch > $ch;
  > hg add $ch;
  > hg ci -m "added "$ch;
  > done;

  $ cd ..
  $ hg init userbar
  $ cd userbar
  $ unset HGUSER
  $ echo "[ui]" >> ./.hg/hgrc
  $ echo "username = bar <bar@test.com>" >> ./.hg/hgrc
  $ hg pull ./../userfoo -q

  $ cd ../userfoo
  $ hg up -r "desc('added b')"
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo c > c
  $ echo e > e
  $ hg add c e
  $ hg ci -m "added c e"
  created new head

  $ hg up -r "desc('added b')"
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo cc > c
  $ hg add c
  $ hg ci -m "added c"
  created new head

  $ hg prune -r "min(desc('added c'))" -s "desc('added c e')"
  1 changesets pruned
  $ hg prune -r "min(desc('added c'))" -s "max(desc('added c'))" --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg glog
  @  4:6c06cda6dc99 added c
  |   draft content-divergent
  |
  | *  3:0c9267e23c9d added c e
  |/    draft content-divergent
  |
  o  1:1740ad2a1eda added b
  |   draft
  |
  o  0:f863f39764c4 added a
      draft
  

  $ cd ../userbar
  $ hg pull ./../userfoo -q
  2 new content-divergent changesets

  $ hg evolve --content-divergent --any
  merge:[3] added c e
  with: [4] added c
  base: [2] added c
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

Make sure resultant cset don't replace the initial user with user running the command:
  $ hg log -r tip
  changeset:   5:443bd2972210
  tag:         tip
  parent:      1:1740ad2a1eda
  user:        foo <foo@test.com>
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added c e
  
  $ cd ..

Testing the three way merge logic for user of content divergent changesets
--------------------------------------------------------------------------

  $ hg init mergeusers
  $ cd mergeusers
  $ for ch in a b c; do
  > touch $ch
  > hg add $ch
  > hg ci -m "added "$ch
  > done;

  $ hg amend -m "updated c"
  $ hg up -r 'desc("added c")' --hidden -q
  updated to hidden changeset 2b3c31fe982d
  (hidden revision '2b3c31fe982d' was rewritten as: 464e35020fd0)
  working directory parent is obsolete! (2b3c31fe982d)
  $ echo coco > c

1) when one user is different wrt base
--------------------------------------

Insert a diverging author name:
  $ hg amend -u 'foouser'
  2 new content-divergent changesets

Run automatic evolution:
  $ hg evolve --content-divergent
  merge:[3] updated c
  with: [4] added c
  base: [2] added c
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 932d6ceb7672

  $ hg log -r tip | grep "^user"
  user:        foouser

  $ hg strip . -q --config extensions.strip=
  2 new content-divergent changesets

2) when both the user are different wrt base
--------------------------------------------

  $ hg up -r 'max(desc("updated c"))'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg amend -u 'baruser'

Run automatic evolution:
  $ hg evolve --content-divergent
  merge:[4] added c
  with: [5] updated c
  base: [2] added c
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 202a770d8c1f

  $ hg log -r tip | grep "^user"
  user:        baruser, foouser

  $ cd ..
