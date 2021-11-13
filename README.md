# NOTE CONTAINER
### Description:
#### Note Container Handle Your Notes & Sections, Powered by Container Use Zip. Other App Active (`hash`, `now`, `key`,`container` or `archive`). Default Run Active in Note Container Command For Other App Type First Argument App Name You Want Be Use.  
---
## APPLICATION FUNCTINALITY

Default Run Note Container See `NOTE CONTAINER`, If Need Other Functionality `container`, `hash`, `key`, `now` Passed Name as First Arguments App You Want Run.

---

## NOTE CONTAINER:

#### Note Container Store Your Data `Note` or `Sections` In Container

Store Your Data `Text` or `Section` In Container

> **Commands :**
>
> >**CONNECT CONTAINER**
> >
> >**path :** positional argument `note container` if not exists created new one
> >
> >**key :** positional argument `secure data`
>
> > **OPTIONS**
> >
> > **--all_names, -A :** Get All Member Names
> >
> > **--all_updated, -Au :** Get All Updated Names
> >
> > **--all_note_updated, -Nu :** Get All Note Updated Names
> >
> > **--all_section_updated, -Su :** Get All Section Updated Names
> >
> > **--all_update_history, -Uh :** All Updated History
> >
> > **--update_history, -uh :** Member Update History - `member name`
> >
> > **--name_filter, -nf :** All Named Filter By Type - chose `section`, `note`
> >
> > **--add_note, -an :** Add Note - `name`, `text`
> >
> > **--get, -g :** Get Any Member Note or Section - `member name`
> >
> > **--get_info, -gi :** Get Member Info - `member name`
> >
> > **--update_note, -un :** Update (Replace) Existed Note Member - `member name`, `new text`
> >
> > **--sorted, -S :** Sorted Member Name With Date - chose `make`,`update`
> >
> > **--reverse_sort, -R:** Reverse Sort Options
> >
> > **--sort_type, -T :** Filter Sort Options By Type - chose `note`, `section`
> >
> > **--append_note, -pn :** Append Text into The Existed Note - `member name`, `text`
> >
> > **--add_section, -as :** Add Section - `member name`, `section data`
> >
> > **--update_section, -us :** Update (Replace) Existed Section - `member name`, `new section data`
> >
> > **--append_section, -ps :** Append & Update Existed Section With New Data - `member name`, `update section data`
> >
> > **--info, -i :** Container Info
> >
> > **--delete, -D :** Remove Member if Exists if not exists pass
> >
> > **--clear, -C :** Clear Container From Any Member
> >
> > **--hash_algorithm, -ha :** Key Hash Algorithm default is SHA3_512 - chose `sha256`, `md5`, `sha3_512`
> >
> > **--time, -t :** Execute Order Time
> >
> > **--verbose, -v :** Verbose

#### What is Section ?? Section Is Key Value Object Exactly Python Dictionary Follow  Python Dictionary Syntax as String . Sections Is Ready :)

Section : {'One': 1, 1:'One', 'byte': b'This Bytes', 'list': [1, 2, 3 , 'A', b'x']}

---

## CONTAINER :

Switch Command `container`, `archive`

> **Commands :**
>
> > **CONNECT CONTAINER**
> >
> > **path :** positional argument `note container` if not exists created new one
> >
> > **--replace, -R :** Replace Member if Exists default is False
>
> > **Options :**
> >
> > **--add, -a :** Add Member - `member name`, `text`
> >
> > **--delete, -D :** Delete Member if Exists if not Pass - `member name`
> >
> > **--all_member, -A :** All Member Names
> >
> > **--extract, -e :** Extract Member To a Path - `member name`, `path`
> >
> > **--get, -g :** Grab Data From Member In Container - `member name`
> >
> > **--append, -ap :** Append Data To Existed Member or Create If not Exists - `member name`, `text`
> >
> > **--update, -u :** Update (Replace) Data From Exists Member - `member name`, `text`
> >
> > **--clear, -C :** Clear Container (Archive) from Any Members

---

## KEY :

Switch Command `key`

> **Commands :**
>
> > **Options :**
> >
> > **--length, -l :** Generated Key Length defaults is `32`
> >
> > **--packsize, -p :** Size Unit For Generate key defaults is `16`
> >
> > **--many, -m :** How Many Key Need defaults is `1`
> >
> > **--chars, -c :** Customize Valid Character default is `ASCII ALPHABET` 
> >
> > **--file, -f :** Path File If Want To Save Generated Key - `Path`

---

## HASH :

Switch Command `hash`

> **Commands :**
>
> > **POSITINAL :**
> >
> > **input :** Input String For Hash Or File Path For Hashed File
> >
> > **Options :**
> >
> > **--algorithm, -a :** Hash Algorithm Defaults is `SHA256` - All Support `sha256`, `sha3_512`, `md5`
> >
> > **--file, -f :** Input Is A File Path

---

## NOW :

Switch Command `now`

> **Commands:**
>
> > **Options :**
> >
> > **--timestamp, -T :** Return Float Time

---

