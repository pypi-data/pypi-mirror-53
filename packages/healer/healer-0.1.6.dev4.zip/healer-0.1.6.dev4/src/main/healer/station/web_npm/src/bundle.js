/**
 * webpack bundle assembly
 */

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'

import VeeValidate from 'vee-validate'
import BootstrapVue from 'bootstrap-vue'

import VuexPersistence from 'vuex-persist'

import axios from 'axios'
import VueAxios from 'vue-axios'

import VueGate from 'vue-gate'
import VueAuthenticate from 'vue-authenticate'

import VueTimers from 'vue-timers'

import VueDraggable from 'vuedraggable'

import VueIdleMixin from 'idle-vue'


// https://fontawesome.com/icons?d=gallery&m=free
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library as FontLibrary } from '@fortawesome/fontawesome-svg-core'
import { 
	faHeartbeat,
	faUser,
	faUserCog,
	faUserEdit,
	faUserPlus,
	faUserShield,
	faSignInAlt,
	faSignOutAlt,
} from '@fortawesome/free-solid-svg-icons'

FontLibrary.add(
		faHeartbeat,
		faUser,
		faUserCog,
		faUserEdit,
		faUserPlus,
		faUserShield,
		faSignInAlt,
		faSignOutAlt,
)

export {
	axios,
	Vue, 
	Vuex,
	VueRouter,
	VeeValidate,
	BootstrapVue,
	VuexPersistence,
	VueAxios,
	VueGate,
	VueAuthenticate,
	VueTimers,
	VueDraggable,
	VueIdleMixin,
	//
	FontAwesomeIcon,
	//
}
