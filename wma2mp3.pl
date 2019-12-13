#!/usr/bin/perl -w
# Script perl parcourant toute une arborescence pour transcoder les wma en mp3
# Utilise mplayer pour transformer en wave
# Utilise le package lame pour réencoder en mp3
use strict;

ReadRep('.');
exit;

sub ReadRep
{
    my ($Dir) = @_;
    my (@fichiers,$fic);
    opendir(DIR,$Dir) || return(0);
    @fichiers=readdir(DIR);
    closedir(DIR);         
    foreach $fic (@fichiers)
    {
             if (($fic ne ".") && ($fic ne ".."))
        {
            if (-d "${Dir}/$fic")
            {
                # appel recursif
                ReadRep ("${Dir}/$fic");
            }
   
             elsif ($fic =~ /\.wma$/i)
                 {
                my $base = "${Dir}/$fic";
                $base =~ s/\.wma$//i;
                # wma -> wave
                system "mplayer \"$base.wma\" -ao pcm:file=/tmp/tmp.wav";
                # wave -> mp3
                system "lame -h /tmp/tmp.wav \"$base.mp3\"";
                unlink("/tmp/tmp.wav");
            }
        }
    }
   
}
