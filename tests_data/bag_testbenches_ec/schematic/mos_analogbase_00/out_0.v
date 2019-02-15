


module nmos4_18(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_svt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_lvt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_hvt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_standard(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_fast(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module nmos4_low_power(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_18(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_svt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_lvt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_hvt(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_standard(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_fast(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule

module pmos4_low_power(
    inout B,
    inout D,
    inout G,
    inout S
);
endmodule


module PYTEST(
    inout  wire b,
    inout  wire d,
    inout  wire g,
    inout  wire s
);

nmos4_lvt XM (
    .B( b ),
    .D( d ),
    .G( g ),
    .S( s )
);

endmodule
