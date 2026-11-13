/* DevLeague Moodle helper: paste into the browser (Claude in Chrome javascript_tool) on any learn.devleague.com page
   while signed in as site admin. Everything goes through Moodle's own web forms with the page's sesskey, so it
   does exactly what clicking would do, and Moodle's own validation still applies. Nothing here changes site settings.

   Load:   (paste this file)            -> window.ML
   Files:  ML.fileInput()               -> adds a hidden <input type=file id="ml-files">; fill it with the
                                           file_upload tool (paths from the workspace), then ML.files() returns them by name.
   Main calls (all async; each returns plain JSON you can read in the tool result):
     ML.sections(courseid)                         section number -> {id, name}
     ML.cms(courseid)                              every activity: {cmid, mod, name, section}
     ML.qcats(courseid)                            question categories: name path -> id (and context id)
     ML.importQuestions(courseid, file, 'gift'|'xml', catPath?)   question import, returns the result text
     ML.addModule(courseid, section, modname, set, files)          new activity from the "Add an activity" form
     ML.copySettings(modelCmid, targetCmid, keep)                  copy a model activity's settings (keeps name/intro by default)
     ML.update(cmid, set, files)                                   change fields on an existing activity's settings form
     ML.addRandom(quizCmid, catId, n, page)                        add n random questions from one category (no subcategories)
     ML.slots(quizCmid)                                            slot list with question/category names, in order
     ML.importGlossary(cmid, file)                                 glossary "Import entries" (XML), into this glossary
   `set` is {fieldname: value} using the form's own field names (open the form and read the names once with ML.fields(url)).
   `files` is {draftFieldName: [File, ...]} for file pickers (e.g. {files: [pdf]} on a File resource, {introattachments: [...]}).
   Driven by the course's moodle.json (tools/moodle/moodle_plan.py prints each step's call). */
(() => {
  const ML = {};
  const sk = () => M.cfg.sesskey;
  const W = M.cfg.wwwroot;
  ML.get = async (url) => new DOMParser().parseFromString(await (await fetch(url, {credentials: 'same-origin'})).text(), 'text/html');

  // ---------- files ----------
  ML.fileInput = () => {
    let i = document.getElementById('ml-files');
    if (!i) { i = Object.assign(document.createElement('input'), {type: 'file', id: 'ml-files', multiple: true}); i.style.display = 'none'; document.body.appendChild(i); }
    return 'ready: fill #ml-files with file_upload';
  };
  ML.files = () => Object.fromEntries([...(document.getElementById('ml-files')?.files || [])].map(f => [f.name, f]));
  ML.file = (name) => ML.files()[name] || (() => { throw new Error('not staged: ' + name); })();

  // ---------- forms ----------
  ML.formData = (form) => {
    const fd = new FormData();
    for (const el of form.elements) {
      if (!el.name || el.disabled) continue;
      if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) continue;
      if (el.type === 'submit' || el.type === 'button' || el.type === 'file') continue;
      if (el.tagName === 'SELECT' && el.multiple) { [...el.selectedOptions].forEach(o => fd.append(el.name, o.value)); continue; }
      fd.append(el.name, el.value);
    }
    return fd;
  };
  ML.fields = async (url) => {
    const f = (await ML.get(url)).querySelector('form.mform');
    return [...f.elements].filter(e => e.name).map(e => `${e.name}=${e.type === 'checkbox' ? e.checked : e.value}`.slice(0, 120));
  };
  const setAll = (fd, set) => {
    for (const [k, v] of Object.entries(set || {})) {
      fd.delete(k);
      if (Array.isArray(v)) v.forEach(x => fd.append(k, x)); else if (v !== null) fd.append(k, v);
    }
  };
  ML.draftUpload = async (file, itemid, ctxid) => {
    const fd = new FormData();
    fd.append('repo_upload_file', file, file.name); fd.append('sesskey', sk()); fd.append('repo_id', await ML.findUploadRepo());
    fd.append('itemid', itemid); fd.append('ctx_id', ctxid || M.cfg.contextid); fd.append('savepath', '/'); fd.append('title', file.name);
    const r = await (await fetch(`${W}/repository/repository_ajax.php?action=upload`, {method: 'POST', body: fd, credentials: 'same-origin'})).json();
    if (r.error) throw new Error('upload ' + file.name + ': ' + r.error);
    return r.file || file.name;
  };
  ML.uploadRepoId = null;
  ML.findUploadRepo = async () => {  // the "Upload a file" repository instance id, read from any filepicker options on a form page
    if (ML.uploadRepoId) return ML.uploadRepoId;
    const html = await (await fetch(`${W}/user/files.php`)).text();
    const m = html.match(/"id":"?(\d+)"?,"name":"Upload a file"/) || html.match(/"name":"Upload a file"[^}]*?"id":"?(\d+)/);
    if (!m) throw new Error('upload repository not found');
    return (ML.uploadRepoId = m[1]);
  };
  const postForm = async (form, fd) => {
    const res = await fetch(new URL(form.getAttribute('action'), W + '/course/').href, {method: 'POST', body: fd, credentials: 'same-origin'});
    const doc = new DOMParser().parseFromString(await res.text(), 'text/html');
    const err = [...doc.querySelectorAll('.form-control-feedback.invalid-feedback, .error')].map(e => e.innerText.trim()).filter(Boolean);
    return {url: res.url, errors: err, doc};
  };
  const fillFiles = async (form, fd, files, ctxid) => {
    if (!files) return;
    await ML.findUploadRepo();
    for (const [field, list] of Object.entries(files)) {
      const itemid = form.querySelector(`[name="${field}"]`)?.value;
      if (!itemid) throw new Error('no file field ' + field);
      for (const f of list) await ML.draftUpload(f, itemid, ctxid);
    }
  };

  // ---------- course structure ----------
  ML.sections = async (courseid) => {
    const doc = await ML.get(`${W}/course/view.php?id=${courseid}`);
    return Object.fromEntries([...doc.querySelectorAll('li.section, .course-section')].map(s =>
      [s.dataset.number ?? s.dataset.sectionnumber, {id: s.dataset.id, name: (s.querySelector('.sectionname, h3') || {}).innerText?.trim()}]));
  };
  ML.cms = async (courseid) => {
    const r = await fetch(`${W}/lib/ajax/service.php?sesskey=${sk()}&info=core_courseformat_get_state`, {method: 'POST', body: JSON.stringify([{index: 0, methodname: 'core_courseformat_get_state', args: {courseid}}])});
    const st = JSON.parse((await r.json())[0].data);
    const secnum = Object.fromEntries(st.section.map(s => [s.id, s.number]));
    return st.cm.map(c => ({cmid: +c.id, mod: c.module, name: c.name, section: secnum[c.sectionid], visible: c.visible}));
  };
  ML.qcats = async (courseid) => {
    const doc = await ML.get(`${W}/question/bank/managecategories/category.php?courseid=${courseid}`);
    const out = {};
    doc.querySelectorAll('[data-categoryid], li[id^="category"]').forEach(li => {
      const id = li.dataset.categoryid || li.id.replace(/\D/g, ''); const name = (li.querySelector('a, .categoryname, span') || li).innerText.trim().split('\n')[0];
      if (id) out[name] = id;
    });
    const sel = (await ML.get(`${W}/question/bank/importquestions/import.php?courseid=${courseid}`)).querySelector('select[name="category"]');
    if (sel) [...sel.options].forEach(o => { out[o.text.replace(/ /g, ' ').trim()] = o.value; });
    return out;
  };

  // ---------- questions ----------
  ML.importQuestions = async (courseid, file, format, catValue) => {
    const url = `${W}/question/bank/importquestions/import.php?courseid=${courseid}`;
    const doc = await ML.get(url); const form = doc.querySelector('form.mform');
    const fd = ML.formData(form);
    setAll(fd, {format, catfromfile: 1, contextfromfile: 1, matchgrades: 'error', stoponerror: 1});
    if (catValue) setAll(fd, {category: catValue});
    await fillFiles(form, fd, {newfile: [file]});
    fd.set('submitbutton', 'Import');
    const r = await postForm(form, fd);
    return (r.doc.querySelector('#region-main') || r.doc.body).innerText.slice(0, 1500);
  };

  // ---------- activities ----------
  ML.addModule = async (courseid, section, modname, set, files) => {
    const url = `${W}/course/modedit.php?add=${modname}&type=&course=${courseid}&section=${section}&return=0&sr=0`;
    const doc = await ML.get(url); const form = doc.querySelector('form.mform');
    const fd = ML.formData(form); setAll(fd, set); await fillFiles(form, fd, files);
    fd.set('submitbutton2', 'Save and return to course');
    const r = await postForm(form, fd);
    if (r.errors.length) return {error: r.errors};
    const after = await ML.cms(courseid);
    const name = set.name; const hit = after.filter(c => c.name === name && c.section == section).pop();
    return {cmid: hit && hit.cmid, name};
  };
  ML.update = async (cmid, set, files) => {
    const doc = await ML.get(`${W}/course/modedit.php?update=${cmid}&return=0`); const form = doc.querySelector('form.mform');
    const fd = ML.formData(form); setAll(fd, set); await fillFiles(form, fd, files);
    fd.set('submitbutton2', 'Save and return to course');
    const r = await postForm(form, fd);
    return r.errors.length ? {error: r.errors} : {ok: cmid};
  };
  // Copy every setting from a model activity of the same type, except the ones in `keep` (and anything instance-specific).
  ML.copySettings = async (modelCmid, targetCmid, keep = []) => {
    const skip = new Set(['course', 'coursemodule', 'section', 'module', 'modulename', 'instance', 'add', 'update', 'return', 'sr',
      'sesskey', '_qf__mod_quiz_mod_form', 'name', 'introeditor[text]', 'introeditor[format]', 'introeditor[itemid]', 'files', 'introattachments',
      'cmidnumber', 'gradecat', 'grade', ...keep]);
    const model = (await ML.get(`${W}/course/modedit.php?update=${modelCmid}&return=0`)).querySelector('form.mform');
    const mfd = ML.formData(model);
    const doc = await ML.get(`${W}/course/modedit.php?update=${targetCmid}&return=0`); const form = doc.querySelector('form.mform');
    const fd = ML.formData(form);
    const names = new Set([...mfd.keys()].filter(k => !skip.has(k) && !k.startsWith('_qf__')));
    names.forEach(k => { fd.delete(k); mfd.getAll(k).forEach(v => fd.append(k, v)); });
    // checkboxes that are on in the target but off in the model
    [...form.elements].filter(e => e.type === 'checkbox' && e.name && !skip.has(e.name) && e.checked && !mfd.has(e.name)).forEach(e => fd.delete(e.name));
    fd.set('submitbutton2', 'Save and return to course');
    const r = await postForm(form, fd);
    return r.errors.length ? {error: r.errors} : {ok: targetCmid, copied: names.size};
  };

  // ---------- quiz slots ----------
  ML.slots = async (cmid) => {
    const doc = await ML.get(`${W}/mod/quiz/edit.php?cmid=${cmid}`);
    return [...doc.querySelectorAll('li.slot')].map(li => ({slot: li.querySelector('.slotnumber')?.innerText.replace(/\D/g, ''),
      text: (li.querySelector('.questionname, .questiontext, .randomquestioncategory') || li).innerText.trim().replace(/\s+/g, ' ').slice(0, 90),
      page: li.closest('ul.section')?.querySelector('.page')?.innerText}));
  };
  // Random questions through Moodle's own web service (the same call the "Add a random question" dialog makes; Moodle 4.3+).
  // ctx = the course's context id (moodle.json context_id). Tested on Moodle 4.5, Nov 12, 2026.
  ML.addRandom = async (cmid, catId, n, page = 1, ctx = M.cfg.contextid) => {
    const filter = {category: {jointype: 1, values: [String(catId)], filteroptions: {includesubcategories: false}}, hidden: {jointype: 1, values: ['0']}};
    const fc = JSON.stringify({filter, jointype: 2, qpage: 0, qperpage: 100, sortdata: {}, cat: `${catId},${ctx}`, tabname: 'questions'});
    const r = await fetch(`${W}/lib/ajax/service.php?sesskey=${sk()}&info=mod_quiz_add_random_questions`, {method: 'POST', credentials: 'same-origin',
      body: JSON.stringify([{index: 0, methodname: 'mod_quiz_add_random_questions', args: {cmid, addonpage: page, randomcount: n, filtercondition: fc, newcategory: '', parentcategory: ''}}])});
    const j = await r.json();
    return j[0].error ? {error: j[0].exception?.message || JSON.stringify(j[0])} : {ok: n};
  };
  // Maximum grade lives on the quiz's Questions page, not its settings form (ML.update's grade field doesn't change it).
  ML.maxGrade = async (cmid, g) => {
    await fetch(`${W}/mod/quiz/edit.php?cmid=${cmid}`, {method: 'POST', credentials: 'same-origin', body: new URLSearchParams({cmid, savechanges: 'Save', maxgrade: g, sesskey: sk()})});
    return (await ML.get(`${W}/mod/quiz/edit.php?cmid=${cmid}`)).querySelector('input[name=maxgrade]')?.value;
  };
  // Long loops: the browser tool times out after about 45 s, but the page keeps running; check the result afterwards with ML.cms / ML.slots.

  // ---------- glossary ----------
  ML.importGlossary = async (cmid, file) => {
    const doc = await ML.get(`${W}/mod/glossary/import.php?id=${cmid}`); const form = doc.querySelector('form.mform');
    const fd = ML.formData(form); setAll(fd, {dest: 'current', catsincl: 0});
    await fillFiles(form, fd, {file: [file]});
    fd.set('save', 'Submit');
    const r = await postForm(form, fd);
    return (r.doc.querySelector('#region-main') || r.doc.body).innerText.slice(0, 600);
  };

  window.ML = ML;
  return 'ML loaded';
})();
