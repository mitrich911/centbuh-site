(function () {
  // Ориентиры для квиза: только то, что подтверждено (ИП — от 1000 ₽), остальное — после консультации
  function estimate(data) {
    if (data.business === 'ИП' && data.need === 'Ежемесячное обслуживание' && data.staff === 'Нет') {
      return 'Ориентир: <b>от 1000 ₽ в месяц</b>. Бухгалтер уточнит детали и назовёт точную цену.';
    }
    if (data.business === 'Ещё не зарегистрирован') {
      return 'Поможем выбрать форму бизнеса и налоговый режим, зарегистрируем и возьмём учёт с первого дня.';
    }
    return 'Стоимость зависит от объёма операций. Бухгалтер перезвонит и назовёт точную цену — консультация бесплатная.';
  }

  function cleanPhone(v) { return v.replace(/\D/g, ''); }
  function phoneOk(v) { var d = cleanPhone(v); return d.length >= 10 && d.length <= 12; }

  function send(form, msg, btn) {
    var name = form.elements.name, phone = form.elements.phone, consent = form.elements.consent;
    name.classList.toggle('is-bad', !name.value.trim());
    phone.classList.toggle('is-bad', !phoneOk(phone.value));
    msg.className = 'form-msg';
    if (!name.value.trim() || !phoneOk(phone.value)) { msg.textContent = 'Проверьте имя и телефон.'; msg.classList.add('err'); return; }
    if (!consent.checked) { msg.textContent = 'Нужно согласие на обработку данных.'; msg.classList.add('err'); return; }

    btn.disabled = true;
    msg.textContent = 'Отправляем…';
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || 'fail'); }); })
      .then(function () {
        msg.textContent = 'Спасибо! Заявка принята, мы свяжемся с вами в рабочее время (пн–пт, 9:00–17:00).';
        msg.classList.add('ok');
        form.reset();
        if (window.ym && window.YM_ID) window.ym(window.YM_ID, 'reachGoal', 'lead_' + form.elements.source.value);
      })
      .catch(function () {
        msg.innerHTML = 'Не удалось отправить. Позвоните <a href="tel:+79787653981">+7 (978) 765-39-81</a> или напишите в <a href="https://wa.me/79787653981" target="_blank" rel="noopener">WhatsApp</a>.';
        msg.classList.add('err');
      })
      .finally(function () { btn.disabled = false; });
  }

  // Квиз-воронка
  var quiz = document.getElementById('quizForm');
  if (quiz) {
    var steps = quiz.querySelectorAll('.step'), cur = 0;
    var back = document.getElementById('quizBack'), next = document.getElementById('quizNext'), submit = document.getElementById('quizSubmit');
    var bar = document.getElementById('quizBar'), count = document.getElementById('quizCount'), qmsg = document.getElementById('quizMsg');

    function show(i) {
      steps[cur].classList.remove('is-active');
      cur = i;
      steps[cur].classList.add('is-active');
      bar.style.width = ((cur + 1) / steps.length * 100) + '%';
      count.textContent = 'Шаг ' + (cur + 1) + ' из ' + steps.length;
      back.hidden = cur === 0;
      next.hidden = cur === steps.length - 1;
      submit.hidden = cur !== steps.length - 1;
      qmsg.textContent = '';
      if (cur === steps.length - 1) {
        document.getElementById('quizEstimate').innerHTML = estimate({
          business: (quiz.elements.business.value), need: quiz.elements.need.value, staff: quiz.elements.staff.value
        });
      }
    }
    function answered() { return !!steps[cur].querySelector('input[type=radio]:checked'); }

    next.addEventListener('click', function () {
      if (!answered()) { qmsg.className = 'form-msg err'; qmsg.textContent = 'Выберите вариант ответа.'; return; }
      show(cur + 1);
    });
    back.addEventListener('click', function () { show(cur - 1); });
    // Автопереход по клику на вариант
    quiz.addEventListener('change', function (e) {
      if (e.target.type === 'radio' && cur < steps.length - 1) setTimeout(function () { show(cur + 1); }, 220);
    });
    quiz.addEventListener('submit', function (e) { e.preventDefault(); send(quiz, qmsg, submit); });
    show(0);
  }

  var call = document.getElementById('callForm');
  if (call) call.addEventListener('submit', function (e) {
    e.preventDefault();
    send(call, call.querySelector('.form-msg'), call.querySelector('button[type=submit]'));
  });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
