uniform sampler2D u_texture;
varying vec2 v_texcoord;
void main()
{
    // https://qiita.com/kazoo/items/7d4550e18e128e1124b3#glsl%E6%96%87%E6%B3%95texture2d-%E9%96%A2%E6%95%B0

    //float r = texture2D(u_texture, v_texcoord).r;
    //gl_FragColor = vec4(r,r,r,1); // original
    //gl_FragColor = vec4(r-0.5,r-0.5,r,1); // blue
    //gl_FragColor = vec4(r,r-0.5,r-0.5,1); //red
    //gl_FragColor = vec4(r-0.5,r,r-0.5,1); //green

    gl_FragColor = texture2D(u_texture, v_texcoord);

}

