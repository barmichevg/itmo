<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'

const router = useRouter()

const mode = ref('login')

const login = ref('')
const password = ref('')
const password2 = ref('')

const error = ref('')
const loading = ref(false)

function formatError(e, fallback) {
  const d = e?.data
  const errs = Array.isArray(d?.errors) ? d.errors.join(' • ') : ''
  return errs || d?.message || fallback
}

async function submit() {
  error.value = ''

  const l = login.value.trim()
  if (!l) {
    error.value = 'Введите логин'
    return
  }
  if (!password.value) {
    error.value = 'Введите пароль'
    return
  }

  if (mode.value === 'register') {
    if (password.value.length < 4) {
      error.value = 'Пароль должен быть минимум 4 символа'
      return
    }
    if (password.value !== password2.value) {
      error.value = 'Пароли не совпадают'
      return
    }
  }

  loading.value = true
  try {
    if (mode.value === 'login') {
      await api.login(l, password.value)
    } else {
      await api.register(l, password.value)
    }
    await router.push('/main')
  } catch (e) {
    error.value = formatError(
        e,
        mode.value === 'login'
            ? 'Не удалось войти. Проверь логин/пароль.'
            : 'Не удалось зарегистрироваться.'
    )
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="header">
    <h1>Бармичев Григорий Андреевич — P3210</h1>
    <small>Веб-программирование — ЛР4 — Вариант 123</small>
  </div>

  <div class="card">
    <div class="row" style="margin-bottom: 10px;">
      <button
          class="button"
          :class="mode === 'login' ? 'primary' : ''"
          type="button"
          @click="mode = 'login'"
      >
        Вход
      </button>

      <button
          class="button"
          :class="mode === 'register' ? 'primary' : ''"
          type="button"
          @click="mode = 'register'"
      >
        Регистрация
      </button>
    </div>

    <form @submit.prevent="submit">
      <div class="row">
        <div class="field">
          <label>Логин</label>
          <input v-model="login" autocomplete="username" />
        </div>

        <div class="field">
          <label>Пароль</label>
          <input v-model="password" type="password" autocomplete="current-password" />
        </div>

        <div v-if="mode === 'register'" class="field">
          <label>Повтор пароля</label>
          <input v-model="password2" type="password" autocomplete="new-password" />
        </div>
      </div>

      <div class="row" style="margin-top: 12px;">
        <button class="button primary" :disabled="loading" type="submit">
          {{ loading ? 'Подождите…' : (mode === 'login' ? 'Войти' : 'Зарегистрироваться') }}
        </button>

        <span v-if="mode === 'login'" class="hint">
          Тестовый пользователь: <b>admin / admin</b>
        </span>
      </div>

      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>
