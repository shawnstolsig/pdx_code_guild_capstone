import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
          light: {
            primary: colors.red.darken4, // #E53935
            secondary: colors.red.lighten4, // #FFCDD2
            accent: colors.red.accent4, // #3F51B5
            background: colors.grey.lighten2, // Not automatically applied
            error: colors.red.accent3
          },
        },
      },
});
